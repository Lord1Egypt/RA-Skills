# TODOS

## P2 - 实体去重 ✅ DONE

**What**: 智能合并相似实体，添加 frequency 属性

**Why**: 100+ 会话后可能产生大量重复实体，影响查询效率和模式发现质量

**Status**: ✅ DONE (2026-03-27) - 已完成实现并推送

**Implementation**:
- `scripts/entity_dedup.py` - EntityDeduplicator 类
  - `_cosine_similarity()` - 余弦相似度计算
  - `EmbeddingCache` - 24h TTL 嵌入缓存
  - `find_candidates()` - 按类型分组 + O(n²) 相似度比较
  - `merge_pair()` - 保留最早时间戳，累加 frequency，合并 tags/provenance
  - `merged_into` 字段标记被合并实体
- `scripts/utils/llm_client.py` - 添加 `embed()` 方法用于嵌入向量计算
- `tests/test_entity_dedup.py` - 26 个测试全部通过（23 原有 + 3 回归测试）

**Pros**:
- 更紧凑的 KG
- 更好的模式发现（frequency 属性）
- 减少手动维护负担

**Cons**:
- 去重算法复杂度 O(n²)，但 n 较小（按类型分组后）
- 可能误合并相似但不相同的实体 — 使用 0.85 阈值缓解

**Effort**: M (human: 4h / CC: 30min)

**Priority**: P2

**Depends on**: 基础提取器完成

**Usage**:
```bash
# Dry-run (不写入 KG)
python3 scripts/entity_dedup.py run --dry-run

# 实际运行去重
python3 scripts/entity_dedup.py run

# 指定阈值
python3 scripts/entity_dedup.py run --threshold 0.90

# 查看统计
python3 scripts/entity_dedup.py stats
```

**API Note**: 需要 embedding API 支持。GLM-5 模型可能需要在 `OPENAI_BASE_URL` 配置正确的 embeddings 端点路径。

---

## P1 - KG Schema 增强 (strength, decay, provenance) ✅ DONE

**What**: 为 KG 实体添加 strength, decay_rate, provenance 字段，支持 Decay Engine

**Why**: Phase 1b — CEO review 决策，需要为基础的 Decay Engine 和 Memory Health Dashboard 提供数据支撑

**Status**: ✅ DONE (2026-03-23) - 已完成实现并推送

**Effort**: S (human: 1h / CC: 15min)

**Depends on**: Phase 1 (KG Extractor) 完成

---

## P2 - PreferenceEngine 实现 ✅ DONE

**What**: 偏好推断引擎，从对话历史和 KG 实体中推断用户偏好

**Why**: Phase 2 — CEO review 决策，让 agent 记住偏好

**Status**: ✅ DONE (2026-03-23) - 已完成实现并推送

**Effort**: M (human: 2h / CC: 30min)

**Depends on**: Phase 1b (KG Schema 增强)

**Implementation**:
- `scripts/preference_engine.py` - PreferenceEngine 类
- `LLMCache` - LLM 判断结果缓存（30分钟TTL）
- `judge_task_similarity()` - LLM 判断任务相似性
- Preference 实体类型添加到 schema

---

## P2 - PreferenceEngine LLM Cache ✅ DONE

**What**: 为 PreferenceEngine 的 LLM 判断结果添加缓存机制

**Why**: 避免重复 LLM 调用，减少延迟和 API 成本

**Status**: ✅ DONE (2026-03-23) - 已集成到 PreferenceEngine

**Effort**: S (human: 1h / CC: 15min)

**Depends on**: Phase 2 (PreferenceEngine) 实现

---

## P3 - Consolidation 引擎 ✅ DONE

**What**: 从重复 Episode 形成 Semantic Memory (SkillCard)

**Why**: Phase 3 — CEO review 决策，实现"第三天自动执行"

**Status**: ✅ DONE (2026-03-24) - 已完成实现并推送

**Implementation**:
- `scripts/consolidation_engine.py` - ConsolidationEngine 类
- `BlockingIndex` - 多级 blocking 索引高效找候选
- `ConsolidationDecision` - LLM 判断结果
- SkillCard 和 ConflictReview 实体类型添加到 schema
- 保守策略：冲突 → 标记待审核，不自动合并

**Effort**: M (human: 4h / CC: 1h)

**Priority**: P3

**Depends on**: Phase 2 (PreferenceEngine)

---

## P1 - Memory Decay 引擎 ✅ DONE

**What**: 实现 Decay Engine — 遗忘低价值记忆

**Why**: CEO review 决策 — 防止记忆无限增长

**Status**: ✅ DONE (2026-03-25) - 已完成实现并推送

**Effort**: S (human: 2h / CC: 30min)

**Implementation**:
- `scripts/decay_engine.py` - DecayEngine class
- `tests/test_decay_engine.py` - 9 passing tests
- Pre-loads all entities once to avoid O(n²) file reads

**Depends on**: Phase 1b (KG Schema 增强)

---

## P2 - Working Memory 管理 ✅ DONE

**What**: Context Window 分层压缩

**Why**: Phase 5 — CEO review 决策 — 解决 Context Window 约束

**Status**: ✅ DONE (2026-03-25) - 已完成实现并推送

**Effort**: M (human: 3h / CC: 1h)

**Implementation**:
- `scripts/working_memory.py` - WorkingMemoryEngine with 3-level compression
- `scripts/utils/llm_client.py` - Shared LLM client (DRY)
- `tests/test_working_memory.py` - 37 passing tests
- Level 1: Full content, Level 2: LLM summary, Level 3: KG key facts

**Depends on**: Phase 4 (Decay Engine)

---

## P1 - 主动记忆恢复 ✅ DONE

**What**: Agent 启动时 staged loading

**Why**: Phase 6 — CEO review 决策 — agent 主动恢复记忆

**Status**: ✅ DONE (2026-03-25) - 已完成实现并推送

**Implementation**:
- `scripts/memory_loader.py` - MemoryLoader class with 3-stage loading
- `tests/test_memory_loader.py` - 19 passing tests
- Stage 1: Core identity (preferences, recent decisions/lessons, strength >= 0.8, within 30 days)
- Stage 2: Episodic memory (decisions by project, pending commitments, findings strength >= 0.5)
- Stage 3: Semantic memory (SkillCards strength >= 0.5, proactive hints)
- Graceful degradation: KG unavailable returns empty results + error field

**Effort**: M (human: 3h / CC: 1h)

**Priority**: P1

**Depends on**: Phase 3 (Consolidation) + Phase 5 (Working Memory)

---

## P2 - Memory Health Dashboard CLI ✅ DONE

**What**: 实现 memory_dashboard.py — 显示记忆强度分布、Consolidation 进度、存储使用统计

**Why**: Phase 7 — CEO review 采纳的扩展，让用户"看到"记忆系统状态

**Status**: ✅ DONE (2026-03-26) - 已完成实现并推送

**Implementation**:
- `scripts/memory_dashboard.py` - MemoryDashboard 类，5 种视图
  - `summary` (默认) / `full` / `decay` / `compact` / `json`
- `tests/test_memory_dashboard.py` - 18 个测试全部通过
- Health Score 计算（Grade A-F）、记忆强度直方图、Consolidation 进度、存储统计、衰减预测（30天）、年龄分布、标签云、来源分类

**Pros**:
- 用户可见性，建立信任
- 理解为什么 agent 记得/忘记某些事

**Cons**:
- 需要定期运行或作为服务启动

**Effort**: S (human: 2h / CC: 1h)

**Priority**: P2

**Depends on**: Phase 1b (KG Schema 增强)