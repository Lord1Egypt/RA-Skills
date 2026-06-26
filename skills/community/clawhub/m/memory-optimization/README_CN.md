# Memory Optimization — 记忆进化基座

记忆系统不只是存储——是真正的进化。让 agent 从"每次像第一次见面"进化到"像一个越来越了解你的老朋友"。

## Vision

第三天重复任务时 agent **自动用之前成功的方式执行**，不需要提醒。记忆有生命：会生长、会衰减、会遗忘、会 Consolidate 成真正的智慧。

## Three-Layer Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Working Memory (Context Window)                             │
│  当前会话完整内容 — 分层压缩：完整 → 摘要 → 关键事实        │
└─────────────────────────────────────────────────────────────┘
                          ↓ Consolidation (N次重复后)
┌─────────────────────────────────────────────────────────────┐
│  Episodic Memory (KG Entities)                              │
│  Decision, Finding, LessonLearned, Commitment              │
│  + strength, decay_rate, provenance                         │
└─────────────────────────────────────────────────────────────┘
                          ↓ Consolidation
┌─────────────────────────────────────────────────────────────┐
│  Semantic Memory (SkillCards)                               │
│  从 Episodic 归纳出的通用模式                               │
└─────────────────────────────────────────────────────────────┘
```

**Memory Decay**: strength 随时间衰减，防止无用记忆占据空间
**Poisoning Protection**: provenance 追踪来源，Consolidation 前验证冲突

## Phase Build Status

| Phase | Feature | Status |
|-------|---------|--------|
| Phase 1 | KG Extractor (会话 → KG) | ✅ Done |
| Phase 1b | KG Schema (strength, decay, provenance) | ✅ Done |
| Phase 2 | Preference Engine (偏好推断) + Entity Deduplication | ✅ Done |
| Phase 3 | Consolidation Engine (Episode → SkillCard) | ✅ Done |
| Phase 4 | Decay Engine (遗忘机制) | ✅ Done |
| Phase 5 | Working Memory (Context 压缩) | ✅ Done |
| Phase 6 | Memory Loader (主动恢复) | ✅ Done |
| Phase 7 | Memory Dashboard (健康仪表盘) | ✅ Done |

## Features

| Feature | Description |
|---------|-------------|
| **KG Extractor** | LLM-driven entity extraction from agent session logs |
| **Knowledge Graph** | Entity relationships with strength, decay, provenance |
| **Entity Deduplication** | Embedding-based duplicate merging (cosine similarity) |
| **Consolidation Engine** | Episode patterns → SkillCards, with conflict detection |
| **Decay Engine** | Automatic strength decay, weak entity archiving |
| **Working Memory** | Context window layered compression (3 levels) |
| **Memory Loader** | 3-stage proactive memory recovery at startup |
| **Memory Dashboard** | Health score, strength histogram, decay forecast |
| **Daily Cleanup** | 3-minute automated maintenance |

## Quick Start

```bash
# Run daily memory cleanup
./scripts/daily-cleanup.sh

# View memory health dashboard
python3 scripts/memory_dashboard.py

# Deduplicate KG entities (dry-run first)
python3 scripts/entity_dedup.py run --dry-run

# Query the knowledge graph
python3 scripts/memory_ontology.py query --tags "#memory"

# Extract entities from session logs
python3 scripts/kg_extractor.py --agents-dir agents/
```

## Memory Dashboard

```bash
python3 scripts/memory_dashboard.py              # 摘要视图 (默认)
python3 scripts/memory_dashboard.py full         # 完整视图
python3 scripts/memory_dashboard.py decay        # 衰减预测
python3 scripts/memory_dashboard.py compact      # 紧凑视图
python3 scripts/memory_dashboard.py json        # JSON 输出
```

**用户可见的记忆系统状态面板**：

```
┌─────────────────────────────────────────────────────────┐
│  记忆健康仪表盘                                           │
├─────────────────────────────────────────────────────────┤
│  📊 记忆强度分布                                          │
│     Decision: ████████████░░░░ 78%                      │
│     LessonLearned: ██████████░░░░░░ 62%                  │
│     SkillCard: ████████████████ 95%                      │
│                                                          │
│  🔄 Consolidation 进度                                    │
│     等待归纳: 12 个实体                                   │
│     已形成技能: 3 个                                      │
│                                                          │
│  🗑️ 最近衰减                                            │
│     - Finding "API变化": 强度 0.15 → 归档候选           │
│     - LessonLearned "性能技巧": 强度 0.22 → 衰减中       │
│                                                          │
│  💾 存储使用                                            │
│     KG 实体: 790 个                                      │
│     总大小: 2.3 MB                                       │
└─────────────────────────────────────────────────────────┘
```

**用户价值**：
- "看到"记忆系统在进化，建立信任
- 理解为什么 agent 记得/忘记某些事
- 手动触发 consolidation 或调整 decay 阈值

## Requirements

- Python 3.8+
- PyYAML

## Documentation

- [SKILL.md](SKILL.md) — Full skill definition and usage guide
- [CLAUDE.md](CLAUDE.md) — Project guidance for Claude Code
- [scripts/README.md](scripts/README.md) — All scripts with usage examples
- [references/](references/) — Implementation guides and templates

## Architecture Highlights

**Decay Rates by Type**:
- Decision: 慢衰减 (0.95/月)
- SkillCard: 慢衰减 (0.99/月)
- LessonLearned: 中等 (0.90/月)
- Finding: 快衰减 (0.80/月)

**Consolidation Strategy**: 冲突 → 标记待审核，不自动合并 (Memory Poisoning 防护优先)

**Active Recovery**: Stage 1 启动时加载 (核心身份) → Stage 2/3 按需加载

## 多 Agent KG 共享

多 agent 场景下 (main, altas, scribe, tutor)，可共享单一知识图谱：

```bash
# 创建共享目录
mkdir -p ~/.openclaw/shared-kg

# 链接主 KG
ln -sf ~/.openclaw/workspace/memory/ontology/graph.jsonl ~/.openclaw/shared-kg/main-kg.jsonl
```

各 agent 的 `TOOLS.md` 应引用：
```markdown
## Knowledge Graph (KG)

- **共享 KG**: ~/.openclaw/shared-kg/main-kg.jsonl
- 包含所有重要的长期记忆、决策、经验教训
```

脚本使用: `KG_DIR=~/.openclaw/shared-kg/ python3 scripts/memory_ontology.py query --tags "#decision"`

## File Structure

```
memory-optimization/
├── SKILL.md                    # Skill definition
├── CLAUDE.md                   # Claude Code guidance
├── README.md                   # This file
├── VERSION                     # Current version
├── CHANGELOG.md               # Version history
├── TODOS.md                    # Project roadmap
├── scripts/
│   ├── daily-cleanup.sh       # Daily maintenance
│   ├── memory_ontology.py      # KG management CLI
│   ├── kg_extractor.py        # Session → KG extraction
│   ├── entity_dedup.py         # Embedding-based dedup
│   ├── consolidation_engine.py # Episode → SkillCard
│   ├── decay_engine.py         # Strength decay
│   ├── memory_loader.py        # Staged recovery
│   ├── memory_dashboard.py      # Health dashboard
│   └── utils/llm_client.py     # Unified LLM client
├── tests/                      # Test suite
├── ontology/                   # KG schema & templates
└── references/                 # Implementation docs
```

## Version

Current: **1.0.2** — See [CHANGELOG.md](CHANGELOG.md) for full history.
