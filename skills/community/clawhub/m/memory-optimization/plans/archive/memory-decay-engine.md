# Memory Decay Engine Plan

## Context

CEO review 决策：防止记忆无限增长，实现 Decay Engine。

**已有基础设施 (Phase 1b)**:
- Schema: `strength`, `decay_rate`, `last_accessed` 字段已定义
- `memory_ontology.py`: `apply_decay_to_entity()`, `refresh_entity_strength()`, `get_entities_by_strength()` 已实现
- DECAY_RATES, DECAY_THRESHOLD 常量已定义

**触发方式**:
- 访问时实时衰减 (access-time real-time decay)
- 每周完整性检查 (weekly integrity check)

---

## 实现方案

### 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Memory Decay Engine                      │
├─────────────────────────────────────────────────────────────┤
│  1. Access-time Decay (实时)                                │
│     └─ get_entity() 调用时计算并应用衰减                    │
│                                                             │
│  2. Batch Decay Engine (定期)                              │
│     └─ decay_engine.py --weekly                            │
│     └─ 扫描所有实体，应用衰减                              │
│     └─ 标记 weak 实体 (strength < threshold)                 │
│     └─ 支持 --dry-run 模拟运行                             │
└─────────────────────────────────────────────────────────────┘
```

### 文件变更

| File | Change |
|------|--------|
| `scripts/memory_ontology.py` | 修改 `get_entity()` 实现访问时衰减 |
| `scripts/decay_engine.py` | 新增：批量衰减引擎 |
| `tests/test_decay_engine.py` | 新增：衰减引擎测试 |

---

## Step 1: 修改 `get_entity()` 实现访问时衰减

### 当前行为
`get_entity()` 调用时 `refresh_entity_strength()` 将 strength 重置为 1.0（无论上次访问过了多久）。

### 新行为
1. 计算 `last_accessed` 到现在经过的时间
2. 如果 `last_accessed` 存在且超过阈值（如 1 小时），应用衰减
3. 如果衰减后 strength < threshold，标记为 weak
4. 如果 `last_accessed` 不存在或刚访问过（<1小时），不衰减

### 代码变更 (`memory_ontology.py`)

```python
# 在 get_entity() 中，约 line 622

ACCESS_DECAY_THRESHOLD_HOURS = 1  # 访问超过1小时才触发衰减

def get_entity(entity_id: str, refresh_strength: bool = True) -> Optional[Dict]:
    entity = _read_entity_from_graph(entity_id)  # 新增：内部读取方法
    if not entity:
        return None

    # 访问时实时衰减
    if refresh_strength:
        last_accessed = entity['properties'].get('last_accessed')
        if last_accessed:
            last_dt = datetime.fromisoformat(last_accessed.replace('Z', '+00:00'))
            hours_elapsed = (datetime.now().astimezone() - last_dt).total_seconds() / 3600

            if hours_elapsed >= ACCESS_DECAY_THRESHOLD_HOURS:
                # 应用衰减（但不要重置到1.0，而是乘以衰减系数）
                days_elapsed = hours_elapsed / 24.0
                apply_decay_to_entity(entity_id, days_elapsed, dry_run=False)

                # 重新读取以获取更新后的值
                entity = _read_entity_from_graph(entity_id)
        else:
            # 首次访问，初始化 strength
            refresh_entity_strength(entity_id)
            entity = _read_entity_from_graph(entity_id)
```

注意：需要新增 `_read_entity_from_graph()` 辅助方法，从 graph.jsonl 中读取实体（不触发衰减）。

---

## Step 2: 新增 `decay_engine.py`

### CLI 接口

```bash
# 每周完整性检查（生产环境）
python3 scripts/decay_engine.py run

# 模拟运行（不写入）
python3 scripts/decay_engine.py run --dry-run

# 查看统计
python3 scripts/decay_engine.py stats

# 查看 weak 实体
python3 scripts/decay_engine.py candidates
```

### 核心功能

1. **`DecayEngine.run()`** - 批量处理所有实体
   - 扫描 graph.jsonl
   - 对每个实体计算并应用衰减
   - 跳过 consolidated_into 的实体
   - 支持 --dry-run

2. **`DecayEngine.apply_decay_all()`** - 应用衰减
   - 对所有实体应用基于时间的衰减
   - 使用 apply_decay_to_entity() 已有函数

3. **`DecayEngine.archive_weak()`** - 归档 weak 实体
   - 找出 strength < DECAY_THRESHOLD 的实体
   - 标记为 `status: archived`
   - 支持 --dry-run

### DecayEngine 类

```python
class DecayEngine:
    def __init__(self, kg_dir: str = None):
        self.stats = {
            'entities_processed': 0,
            'entities_decayed': 0,
            'entities_archived': 0,
            'entities_strength_reset': 0,
        }

    def run(self, dry_run: bool = False) -> Dict:
        """运行完整的 decay cycle"""
        # 1. 应用衰减
        self.apply_decay_all(dry_run)
        # 2. 归档 weak 实体
        self.archive_weak(dry_run)
        return self.stats

    def apply_decay_all(self, dry_run: bool = False):
        """对所有实体应用衰减"""
        for entity_id in self._iter_entity_ids():
            entity = get_entity(entity_id, refresh_strength=False)  # 不触发refresh
            if not entity:
                continue

            # 计算自上次访问以来的衰减
            last_accessed = entity['properties'].get('last_accessed')
            if not last_accessed:
                continue

            # ... 计算并应用衰减

    def archive_weak(self, dry_run: bool = False):
        """归档 weak 实体"""
        weak = get_entities_by_strength(DECAY_THRESHOLD)
        for entity in weak:
            if entity['properties'].get('consolidated_into'):
                continue  # 已被合并，跳过
            # 标记为 archived
```

---

## Step 3: 测试

### 计划测试用例

1. `TestDecayEngine::test_apply_decay_resets_on_access` - 验证访问时重置
2. `TestDecayEngine::test_archive_weak_entities` - 验证归档 weak 实体
3. `TestDecayEngine::test_skip_consolidated` - 验证跳过已合并实体
4. `TestDecayEngine::test_dry_run` - 验证 dry-run 不写入
5. `TestAccessDecay::test_hours_elapsed_calculation` - 验证时间计算

### 审查补充测试用例

6. `TestAccessDecay::test_no_last_accessed_initializes` - 首次访问初始化
7. `TestAccessDecay::test_invalid_last_accessed_format_handled` - 格式错误处理
8. `TestRefreshDecay::test_computes_decay_not_hard_reset` - refresh 计算衰减
9. `TestDecayEngine::test_atomic_write` - 原子写入

---

## 关键设计决策

### 1. 访问时衰减 vs 批量衰减 ✅

**选择方案A** + 每周批量检查兜底
- `ACCESS_DECAY_THRESHOLD_HOURS = 1`

### 2. DecayEngine 职责 ✅

**选择方案A**: 轻量包装器，复用 `memory_ontology` 函数

### 3. refresh_entity_strength 行为 ✅

**选择方案B**: 修改 `refresh_entity_strength()` 计算衰减而非硬重置

### 4. Archived 实体处理 ✅

**选择方案A**: archived 实体仍在 KG 中，不通知 agent

### 5. 衰减阈值 ✅

`ACCESS_DECAY_THRESHOLD_HOURS = 1` (1小时)

### 6. 批量写入 ✅

**选择方案B**: 写入临时文件，原子替换

---

## NOT in Scope

- 衰减通知（未来可扩展）
- 衰减历史记录（已有 provenance）
- 多语言/时区处理（暂用 UTC）

---

## What Already Exists

| 功能 | 文件 | 已有实现 |
|------|------|----------|
| 衰减计算 | `memory_ontology.py` | `apply_decay_to_entity()` ✓ |
| 刷新 strength | `memory_ontology.py` | `refresh_entity_strength()` ✓ |
| 获取 weak 候选 | `memory_ontology.py` | `get_entities_by_strength()` ✓ |
| Strength 分布统计 | `memory_ontology.py` | `get_strength_distribution()` ✓ |
| Schema 定义 | `memory-schema.yaml` | `strength`, `decay_rate`, `last_accessed` ✓ |

---

## 失败模式

| 路径 | 失败场景 | 用户可见性 |
|------|----------|------------|
| Access decay | `last_accessed` 格式错误 | 静默跳过，日志警告 |
| Batch decay | graph.jsonl 损坏 | 报错退出 |
| Archive | 实体不存在 | 静默跳过 |

---

## Effort

- Human: ~2h
- CC: ~30min
