# MemPalace Memory Skill (Enhanced v4)

基于 **MemPalace**（22k⭐ · Benchmark 最高分）融合 SuperMem 增强层的记忆系统。

---

## 系统架构（第一性原理）

```
用户消息
  ↓
[Hook] message:preprocessed
  ↓
mempalace_cli.py  ← 修复后版本（v4）
  ↓ (call /Users/mars/Library/Python/3.9/bin/mempalace)
MemPalace 原生检索
  ↓
Levenshtein 去重（>85%相似度）
  ↓
MMR 多样性重排（λ=0.7）
  ↓
注入 bodyForAgent → 模型响应
```

**关键修复（v4）**：
- ✅ Hook 正确调用 `mempalace_cli.py`（之前错误调用 `super_mem_cli.py`）
- ✅ 移除不存在的 `--no-exact` 参数
- ✅ MMR + 去重 + 清洗 全部启用
- ✅ 删除遗留的 `super_mem_cli.py` 调用

---

## 核心文件

| 文件 | 作用 |
|------|------|
| `scripts/mempalace_cli.py` | 增强CLI（MMR+去重+清洗）← 召回入口 |
| `scripts/mempalace_reranker.py` | MMR重排+Levenshtein去重+元数据剥离 |
| `scripts/super_mem_cli.py` | SuperMem层（ChromaDB bridge，不用于hook） |
| `hook.ts` | OpenClaw hook处理器 |

---

## CLI 命令

```bash
# 增强搜索（MMR + 去重 + 清洗）— 召回链路入口
/usr/bin/python3 ~/.openclaw/workspace/skills/mempalace-memory/scripts/mempalace_cli.py search "查询" --limit 5

# 状态检查
/usr/bin/python3 ~/.openclaw/workspace/skills/mempalace-memory/scripts/mempalace_cli.py status

# 唤醒（启动上下文）
/usr/bin/python3 ~/.openclaw/workspace/skills/mempalace-memory/scripts/mempalace_cli.py wake-up

# 增量挖掘
/usr/bin/python3 ~/.openclaw/workspace/skills/mempalace-memory/scripts/mempalace_cli.py mine

# 删除记忆（ChromaDB forget）
/usr/bin/python3 ~/.openclaw/workspace/skills/mempalace-memory/scripts/mempalace_cli.py forget <memory_id>
```

---

## 增强层详情

| 功能 | 实现 | 状态 |
|------|------|------|
| 自动 hook 注入 | `message:preprocessed` | ✅ v4修复 |
| MMR 多样性重排 | `mempalace_reranker.py` | ✅ |
| Levenshtein 去重 | `mempalace_reranker.py` (>85%) | ✅ |
| 元数据清洗 | `mempalace_reranker.py` | ✅ |
| ChromaDB forget | `mempalace_cli.py` | ✅ |
| BM25+向量混合搜索 | MemPalace 原生 | ✅ |
| 4层记忆栈 | MemPalace 原生 | ✅ |
| Palaces Graph | MemPalace 原生 | ✅ |
| SuperMem bridge | `super_mem_cli.py bridge` | ✅ 可选 |

---

## 数据存储

- **MemPalace 原生**：`~/.mempalace/palace/`（387 drawers，事实来源）
- **SuperMem ChromaDB**：`~/.super-mem/chroma/`（通过bridge同步，可选层）
- **Hook 注册**：`~/.openclaw/hooks/mempalace-recall/handler.ts`

---

## 安装要求

- Python 3.9+
- Node.js
- MemPalace CLI：`/Users/mars/Library/Python/3.9/bin/mempalace`
- Ollama（用于向量嵌入）：`nomic-embed-text` 模型

---

## 注意事项

1. **Hook 入口**：`~/.openclaw/hooks/mempalace-recall/handler.ts` 是 OpenClaw 加载的唯一文件（不是 `hook.ts`）
2. **SuperMem 是可选层**：`super_mem_cli.py` 可独立使用，但不通过 hook 调用
3. **身份文件**：`~/.mempalace/identity.txt` 控制 wake-up 的 L0 层
4. **使用 `trash > rm`** 保护数据

---

## 更新日志

### v4 (2026-04-08)
- **FIX**: Hook 调用 `mempalace_cli.py`（之前错误调用 `super_mem_cli.py`）
- **FIX**: 移除不存在的 `--no-exact` 参数
- **FIX**: MMR + 去重 + 清洗 全部启用
- **CLEAN**: 删除 `BOOTSTRAP.md`
- **ADD**: 创建 `~/.mempalace/identity.txt`
- **ADD**: 完整第一性原理架构文档

### v3 (历史版本)
- SuperMem v4 pure search（已废弃）
