---
name: memory-complete
version: "4.0.0"
description: Complete Memory System - Unified integration of all memory features
author: Erbing
license: MIT
keywords:
  - memory
  - sqlite
  - lancedb
  - tom
  - emotional
  - retrieval
  - gbrain
  - mempalace
  - ollama
category: productivity
requires:
  - python >= 3.7
  - sqlite3
  - lancedb >= 0.3.0 (optional)
  - sentence-transformers >= 2.0.0 (optional)
  - networkx >= 2.0 (optional)
install:
  post_install: |
    # Create database directory
    mkdir -p memory/database
    
    # Initialize database
    python scripts/init_complete_database.py
    
    # Verify installation
    python scripts/verify_complete_install.py
---

# Complete Memory System v4.0

完整记忆系统 - 整合所有记忆相关功能

## 功能特性

### 核心功能
- [OK] **双脑架构** - SQLite（结构化）+ LanceDB（向量）
- [OK] **四层记忆栈** - 工作记忆、情景记忆、语义记忆、程序记忆
- [OK] **四策略检索** - 按需归因、时间衰减、重要性优先、向量语义
- [OK] **Theory of Mind** - 心智模型推理引擎
- [OK] **情感分析** - EQ改进，7种情绪类型
- [OK] **增强检索** - 关键词提取、相关记忆检测
- [OK] **Ollama集成** - 本地模型嵌入（可选）

### GBrain核心
- [OK] **Originals Folder** - 原创想法捕获
- [OK] **Entity Detection** - 实体检测
- [OK] **Brain-First Lookup** - 大脑优先查找
- [OK] **Compiled Truth + Timeline** - 编译真理+时间线
- [OK] **Dream Cycle** - 夜间自动维护

### MemPalace功能
- [OK] **Agent日记系统** - AAAK压缩格式
- [OK] **情感标记系统** - 6种情感标记
- [OK] **历史追溯能力** - 完整时间线

### Ultimate Memory v3.0
- [OK] **多平台接入层** - Feishu、Telegram、Discord等
- [OK] **分层上下文** - 5层上下文管理
- [OK] **自进化系统** - 自动学习和改进
- [OK] **工具注册** - 工具能力管理
- [OK] **互联网获取** - Agent-Reach集成
- [OK] **安全扫描** - CyberMind/HexMind集成（可选）

## 数据库表（20个）

### 核心记忆表（4个）
1. `memories` - 通用记忆
2. `episodic_memories` - 情景记忆
3. `semantic_memories` - 语义记忆（知识图谱）
4. `procedural_memories` - 程序记忆（技能）

### 工作记忆表（1个）
5. `working_memory` - 工作记忆（会话临时）

### Agent日记表（1个）
6. `agent_diary` - Agent日记

### 检索策略表（1个）
7. `retrieval_cache` - 检索缓存

### GBrain表（3个）
8. `originals` - 原创想法
9. `entities` - 实体（人员/公司/概念）
10. `entity_timelines` - 实体时间线

### 上下文表（1个）
11. `layered_context` - 分层上下文

### 自进化表（1个）
12. `evolution_log` - 自进化记录

### 工具注册表（1个）
13. `registered_tools` - 工具注册

### 平台消息表（1个）
14. `platform_messages` - 多平台消息

### 会话摘要表（1个）
15. `session_summaries` - 会话摘要

### 安全扫描表（3个）
16. `security_scans` - 安全扫描
17. `vulnerability_findings` - 漏洞发现
18. `osint_intel` - OSINT情报

### 攻击链表（1个）
19. `attack_chains` - 攻击链

### 配置表（1个）
20. `system_config` - 系统配置

## 安装

### 1. 初始化数据库

```bash
python scripts/init_complete_database.py
```

### 2. 验证安装

```bash
python scripts/verify_complete_install.py
```

## 使用方法

### 基本使用

```python
from complete_memory_system import CompleteMemorySystem

# 初始化
system = CompleteMemorySystem()
system.initialize()

# 添加记忆
mem_id = system.add_memory(
    memory_type="learning",
    title="学习Python",
    content="今天学习了Python基础语法",
    importance=8
)

# 搜索记忆
results = system.search("Python", limit=10)

# 智能搜索（四策略）
smart = system.smart_search("Python", mode="balanced")

# 情感分析
emotion = system.analyze_emotion("I am very happy!")

# 写日记
system.write_diary(
    summary="完成Python学习",
    learnings=["基础语法", "数据结构"],
    decisions=["继续深入学习"]
)

# 添加知识
system.add_knowledge("Python", "is", "programming_language")

# 添加技能
system.add_skill(
    skill_name="Python编程",
    skill_type="programming",
    description="Python编程技能",
    steps=["学习语法", "练习项目", "阅读源码"]
)

# 获取统计
stats = system.get_statistics()

# 关闭
system.close()
```

### 四策略检索

```python
from retrieval_strategies import FourStrategyRetrieval

retrieval = FourStrategyRetrieval()

# 策略1: 按需归因检索
results = retrieval.retrieve_by_attribution("Python")

# 策略2: 时间衰减检索
results = retrieval.retrieve_by_time_decay("Python", half_life_days=30)

# 策略3: 重要性优先检索
results = retrieval.retrieve_by_importance(min_importance=8)

# 策略4: 向量语义检索
results = retrieval.retrieve_by_semantic("Python")

# 智能检索（组合模式）
smart = retrieval.smart_retrieve("Python", mode="balanced")
```

### MemPalace四层记忆

```python
from memory_palace import MemPalace

palace = MemPalace()
palace.connect()

# 添加情景记忆
palace.add_episodic(
    event_type="learning",
    content="学习了MemPalace四层架构",
    emotion="curiosity",
    importance=7
)

# 添加知识（语义记忆）
palace.add_knowledge("MemPalace", "has_layer", "working_memory")

# 添加技能（程序记忆）
palace.add_skill(
    skill_name="记忆管理",
    skill_type="cognitive",
    description="记忆管理技能",
    steps=["分类", "索引", "检索"]
)

# 写日记
palace.write_diary(
    summary="完成MemPalace学习",
    learnings=["四层架构", "AAAK压缩"],
    decisions=["应用到实际项目"]
)

# 获取最近情景
episodes = palace.get_recent_episodes(limit=10)

palace.close()
```

### Theory of Mind

```python
from tom_engine import ToMEngine

tom = ToMEngine()
tom.initialize()

# 更新信念
tom.update_belief(
    entity="user",
    belief_type="preference",
    content="喜欢Python",
    confidence=0.8
)

# 推断意图
intent = tom.infer_intent("user", "我想学习Python")

# 检测情绪
emotion = tom.detect_emotion("user", "I am very happy!")

# 获取信念
beliefs = tom.get_beliefs("user")

tom.close()
```

### 情感分析

```python
from emotional_analyzer import EmotionalAnalyzer

analyzer = EmotionalAnalyzer()

# 分析情感
result = analyzer.analyze("I am very happy with this!")
print(f"情感: {result['primary_emotion']}")
print(f"置信度: {result['confidence']}")

# 检测情感倾向
sentiment, confidence = analyzer.detect_sentiment("This is great!")

# 生成情感响应
response = analyzer.get_emotional_response("I love this!")

# 批量分析
texts = ["I'm happy", "This is bad", "It's okay"]
results = analyzer.batch_analyze(texts)
```

### 增强检索

```python
from enhanced_retrieval import EnhancedRetrieval

retrieval = EnhancedRetrieval()
retrieval.initialize()

# 增强搜索
results = retrieval.search(
    query="Python",
    limit=10,
    min_importance=7,
    category="learning",
    days_old=30
)

# 语义搜索
results = retrieval.semantic_search("编程语言", limit=10)

# 获取相关记忆
related = retrieval.get_related_memories(memory_id=123, limit=5)

# 获取热门记忆
trending = retrieval.get_trending_memories(days=7, limit=10)

# 获取统计
stats = retrieval.get_statistics()

retrieval.close()
```

### Ollama嵌入（可选）

```python
from ollama_embedding import OllamaEmbedding

ollama = OllamaEmbedding(model="nomic-embed-text")

# 检查连接
if ollama.check_connection():
    # 生成嵌入
    embedding = ollama.embed("Python is great")
    print(f"维度: {len(embedding)}")

    # 批量生成
    embeddings = ollama.embed_batch(["Python", "Java", "C++"])

    # 计算相似度
    sim = ollama.similarity(embedding1, embedding2)
    print(f"相似度: {sim:.2f}")
```

## 配置

### 系统配置

```python
config = {
    'use_ollama': True,
    'ollama_model': 'nomic-embed-text',
    'ollama_url': 'http://localhost:11434',
    'min_confidence': 0.3,
    'cleanup_interval_days': 90
}

system = CompleteMemorySystem(config=config)
```

### Ollama推荐模型

- `nomic-embed-text` - 轻量级（274MB，768维）
- `mxbai-embed-large` - 高精度（669MB，1024维）
- `all-minilm` - 超轻量（120MB，384维）

## 架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    统一记忆系统 v4.0                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │            接入层 (Access Layer)                         │   │
│  │  Feishu | Telegram | Discord | Matrix | Email | Web    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↓                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │            四层记忆栈 (Four-Layer Memory Stack)          │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │   │
│  │  │ 工作记忆 │ │ 情景记忆 │ │ 语义记忆 │ │ 程序记忆 │       │   │
│  │  │ Working │ │ Episodic│ │ Semantic│ │Procedural│      │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘       │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │         Agent 日记 (AAAK 压缩格式)              │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↓                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │            检索层 (Retrieval Layer)                      │   │
│  │  四策略检索 + 智能检索模式 + 语义搜索                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↓                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │            智能层 (Intelligence Layer)                   │   │
│  │  ToM心智模型 | 情感分析 | 自进化 | 实体检测            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↓                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │            上下文层 (Context Layer)                      │   │
│  │  5层上下文：Session | Task | Project | Global | Meta   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↓                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │            存储层 (Storage Layer)                       │   │
│  │  SQLite (结构化) + LanceDB (向量) + Ollama (本地)      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 文件结构

```
memory/
├── SKILL.md
├── README.md
├── package.json
├── scripts/
│   ├── complete_memory_system.py      # 统一入口
│   ├── retrieval_strategies.py        # 四策略检索
│   ├── memory_palace.py               # MemPalace实现
│   ├── tom_engine.py                  # ToM引擎
│   ├── emotional_analyzer.py          # 情感分析器
│   ├── enhanced_retrieval.py          # 增强检索
│   ├── ollama_embedding.py            # Ollama嵌入
│   ├── init_complete_database.py      # 数据库初始化
│   └── verify_complete_install.py     # 安装验证
├── docs/
│   ├── GBRAIN_GUIDE.md                # GBrain指南
│   ├── GBRAIN_REPORT.md               # GBrain报告
│   ├── MEMPALACE_USAGE.md             # MemPalace使用
│   ├── ULTIMATE_V3.md                 # 终极系统v3.0
│   ├── ARCHITECTURE.md               # 架构文档
│   └── API.md                         # API文档
└── examples/
    └── complete_usage_demo.py
```

## 版本历史

### v4.0 (2026-04-11)
- [OK] 整合所有记忆相关功能
- [OK] 20个数据库表
- [OK] 四层记忆栈
- [OK] 四策略检索
- [OK] ToM心智模型
- [OK] 情感分析
- [OK] GBrain核心
- [OK] MemPalace功能
- [OK] Ultimate Memory v3.0
- [OK] Ollama集成

## 许可证

MIT License

## 作者

Erbing - OpenClaw Workspace Agent

## 贡献

欢迎提交Issue和Pull Request！

## 支持

如有问题，请提交Issue或联系作者。
