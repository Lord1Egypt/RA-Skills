# 弘脑记忆系统 (HongNao Memory OS)

> 为 OpenClaw 平台打造的专属长期记忆系统

## 项目信息

- **项目名称**: 弘脑记忆系统 (HongNao Memory OS)
- **项目代号**: HN-MemOS
- **版本**: v0.2.0
- **启动时间**: 2026 年 4 月 5 日
- **开发状态**: OpenClaw Integration (Day 8/15)
- **技术参考**: EverMemOS (EverMind-AI 开源项目)
- **集成目标**: OpenClaw 平台深度集成

## 快速开始

### 1. 测试完整系统

```bash
cd /Users/tangfeng/.openclaw/workspace/hongnao_memory
python main.py
```

### 2. 测试单个模块

```bash
# 测试记忆抽取
python memory_extraction.py

# 测试记忆巩固
python memory_consolidation.py

# 测试记忆检索
python memory_retrieval.py

# 测试记忆更新与遗忘
python memory_update.py

# 测试 API 接口
python memory_api.py
```

## 核心模块

### 1. 记忆抽取模块 (Memory Extraction)

**文件**: `memory_extraction.py`

**功能**:
- 从对话/任务中自动抽取记忆
- 支持 5 种记忆类型：
  - **事实型 (FACT)**: 用户信息、项目背景
  - **偏好型 (PREFERENCE)**: 表达风格、工作习惯
  - **技能型 (SKILL)**: 已掌握的工具、方法
  - **情感型 (EMOTION)**: 用户反馈、满意度
  - **约束型 (CONSTRAINT)**: 必须遵守的规则

**使用示例**:
```python
from memory_extraction import MemoryExtractor

extractor = MemoryExtractor()
text = "用户叫唐锋，在燧弘华创工作，喜欢简洁风格。"
mem_cells = extractor.extract_from_text(text, source="conversation")

for cell in mem_cells:
    print(f"[{cell.memory_type}] {cell.content}")
```

### 2. 记忆巩固模块 (Memory Consolidation)

**文件**: `memory_consolidation.py`

**功能**:
- **去重**: 合并重复/冲突记忆
- **压缩**: 生成简洁摘要（>200 字截断）
- **关联**: 建立记忆间链接（基于标签）
- **评分**: 多因子重要性重算
- **场景创建**: MemScene 记忆场景

**巩固流程**:
```
原始记忆 → 去重 → 压缩 → 关联 → 评分 → 巩固后记忆
```

**使用示例**:
```python
from memory_consolidation import MemoryConsolidator

consolidator = MemoryConsolidator()
consolidated = consolidator.consolidate(mem_cells)

# 创建场景
scene = consolidator.create_scene(
    title="燧弘华创项目",
    scene_type="project",
    mem_cells=consolidated
)
```

### 3. 记忆检索模块 (Memory Retrieval)

**文件**: `memory_retrieval.py`

**功能**:
- **混合检索**: 语义检索 + 关键词检索
- **多因子评分**: 语义 (50%) + 关键词 (30%) + 时间 (10%) + 重要性 (10%)
- **上下文重建**: 根据检索结果重建记忆上下文
- **按类型/标签检索**: 支持多种检索方式

**检索策略**:
```
召回 = 语义检索 (TopK=20) + 关键词检索 (TopK=10)
重排序 = 语义分数×0.5 + 重要性×0.3 + 时间衰减×0.2
最终返回 = TopK=5-10 条记忆
```

**使用示例**:
```python
from memory_retrieval import HybridRetriever

retriever = HybridRetriever(mem_cells)
results = retriever.retrieve("用户信息和偏好", top_k=5)

for result in results:
    print(f"[{result.final_score:.3f}] {result.mem_cell.content}")

# 重建上下文
context = retriever.rebuild_context(results, max_tokens=1000)
print(context)
```

### 4. 记忆更新与遗忘模块 (Memory Update & Forgetting)

**文件**: `memory_update.py`

**功能**:
- **冲突解决**: 更新/合并/保留策略
- **遗忘曲线**: 基于艾宾浩斯遗忘曲线
- **自动清理**: 清理长期未访问的记忆
- **归档机制**: 低价值记忆归档

**遗忘策略**:
- **时间衰减**: 超过 N 天未访问的记忆降低重要性
- **主动清理**: 重要性<阈值且 N 天未访问的记忆归档/删除
- **冲突解决**: 新记忆覆盖旧记忆，保留版本历史

**使用示例**:
```python
from memory_update import MemoryUpdater, MemoryForgetter

# 更新记忆
updater = MemoryUpdater()
updated_cells, logs = updater.update_memory(existing_cells, new_cells)

# 应用遗忘曲线
forgetter = MemoryForgetter()
keep, updated, archive, delete = forgetter.apply_forgetting(mem_cells)
```

### 5. 统一 API 接口 (Memory API)

**文件**: `memory_api.py`

**功能**:
- 整合所有模块
- 提供统一的高级 API
- 支持导入/导出 JSON
- 系统统计信息

**使用示例**:
```python
from memory_api import HongNaoMemorySystem, MemorySystemConfig

# 创建系统
config = MemorySystemConfig()
system = HongNaoMemorySystem(config)

# 添加记忆
system.add_memories_from_text("用户叫唐锋，喜欢简洁风格。")

# 检索记忆
result = system.retrieve_memories("用户信息", top_k=3)
print(result['context'])

# 导出
json_str = system.export_to_json()
```

## 系统架构

```
┌─────────────────────────────────────────────────┐
│              弘脑记忆系统 (HN-MemOS)             │
├─────────────────────────────────────────────────┤
│  【API 层】                                      │
│  HongNaoMemorySystem - 统一接口                  │
├─────────────────────────────────────────────────┤
│  【核心模块层】                                  │
│  MemoryExtractor    - 记忆抽取                   │
│  MemoryConsolidator - 记忆巩固                   │
│  MemoryRetriever    - 记忆检索                   │
│  MemoryUpdater      - 记忆更新                   │
│  MemoryForgetter    - 记忆遗忘                   │
├─────────────────────────────────────────────────┤
│  【数据模型层】                                  │
│  MemCell  - 记忆颗粒（最小单元）                 │
│  MemScene - 记忆场景（记忆集合）                 │
└─────────────────────────────────────────────────┘
```

## 记忆单元设计

### MemCell (记忆颗粒)

**属性**:
- `id`: 唯一标识
- `content`: 记忆内容
- `memory_type`: 记忆类型
- `source`: 来源
- `created_at`: 创建时间
- `updated_at`: 更新时间
- `importance`: 重要性评分 (1-10)
- `access_count`: 访问次数
- `tags`: 关联标签
- `metadata`: 额外元数据

### MemScene (记忆场景)

**属性**:
- `id`: 唯一标识
- `title`: 场景标题
- `scene_type`: 场景类型 (project/user/task/relationship)
- `memcell_ids`: 包含的 MemCell ID 列表
- `created_at`: 创建时间
- `updated_at`: 更新时间
- `activity_level`: 场景活跃度 (0-1)
- `last_accessed`: 最后访问时间

## 技术栈

- **语言**: Python 3.8+
- **存储**: SQLite + ChromaDB (待集成)
- **向量模型**: BGE-M3 / M3E-Base (待集成)
- **部署**: Docker + Kubernetes (待实现)

## 开发计划

### 阶段一：基础架构 ✅ (第 1-3 天)
- [x] 项目脚手架搭建
- [x] 数据库设计（SQLite + ChromaDB）
- [x] 核心数据模型定义（MemCell/MemScene）
- [x] 基础 API 接口设计

### 阶段二：核心模块 🔄 (第 4-7 天)
- [x] 记忆抽取模块开发 ✅
- [x] 记忆巩固模块开发 ✅
- [x] 记忆检索模块开发 ✅
- [x] 记忆更新/遗忘模块开发 ✅

### 阶段三：平台集成 ⏳ (第 8-10 天)
- [ ] 与燧弘 MaaS 平台对接
- [ ] 与 OpenClaw 集成
- [ ] 6 大 Agent Tool 适配
- [ ] API 文档编写

### 阶段四：测试优化 ⏳ (第 11-13 天)
- [ ] 单元测试
- [ ] 性能测试（召回率/延迟/并发）
- [ ] 记忆质量评估
- [ ] 性能优化

### 阶段五：部署上线 ⏳ (第 14-15 天)
- [ ] 生产环境部署
- [ ] 监控告警配置
- [ ] 用户文档编写
- [ ] 项目验收

## 关键指标 (KPI)

| 指标 | 目标值 | 当前状态 |
|------|--------|----------|
| 召回准确率 | >90% | 待测试 |
| 检索延迟 | <100ms (P95) | 待测试 |
| 记忆压缩率 | >50% | 已实现 |
| Token 节省 | >40% | 待测试 |
| 并发能力 | >1000 QPS | 待实现 |

## 文件结构

```
hongnao_memory/
├── main.py                    # 主入口
├── memory_api.py              # 统一 API 接口
├── memory_extraction.py       # 记忆抽取模块
├── memory_consolidation.py    # 记忆巩固模块
├── memory_retrieval.py        # 记忆检索模块
├── memory_update.py           # 记忆更新与遗忘模块
└── README.md                  # 本文档
```

## 使用示例

### 完整流程示例

```python
from memory_api import HongNaoMemorySystem

# 创建系统
system = HongNaoMemorySystem()

# 添加记忆
system.add_memories_from_text("""
    用户叫唐锋，在燧弘华创工作，职位是执行总裁。
    用户喜欢简洁商务风格，偏好使用 PPT 做演示。
    必须保证数据安全，不能泄露敏感信息。
""")

# 检索记忆
result = system.retrieve_memories("用户偏好", top_k=3)
print(f"检索结果：{result['context']}")

# 更新记忆
system.update_memories("用户现在偏好科技感风格。")

# 创建场景
scene_result = system.create_scene("燧弘项目", "project")
print(f"场景：{scene_result['scene']['title']}")

# 查看统计
stats = system.get_stats()
print(f"总记忆数：{stats['total_memories']}")

# 导出
json_str = system.export_to_json()
```

## 与燧弘平台集成

### 接入 1+N+X 架构

```
┌─────────────────────────────────────────────────────┐
│              OpenClaw 平台                           │
├─────────────────────────────────────────────────────┤
│  【用户交互层】                                      │
│  • Feishu/Telegram/WhatsApp/Discord 等多渠道接入    │
│  • 会话管理 (sessions)  • 工具调用 (tools)          │
├─────────────────────────────────────────────────────┤
│  【弘脑记忆系统 - 深度集成层】                        │
│  • Session 记忆持久化  • 用户偏好学习               │
│  • 工具使用记忆  • 项目上下文记忆                    │
│  • 对话风格学习  • 技能配置记忆                      │
├─────────────────────────────────────────────────────┤
│  【记忆核心层】                                      │
│  • MemCells(记忆颗粒)  • MemScenes(记忆场景)        │
│  • 向量检索 (ChromaDB)  • 关系存储 (SQLite)         │
└─────────────────────────────────────────────────────┘
```

### 专注 OpenClaw 平台集成

**战略调整**：集中资源深耕 OpenClaw 平台，打造深度集成的记忆系统能力。

| 集成模块 | 记忆系统应用场景 |
|----------|------------------|
| **Session 记忆** | 跨会话上下文保留，用户偏好持久化 |
| **Agent 工具记忆** | 工具使用习惯、命令偏好、工作流记忆 |
| **文件/项目记忆** | 项目上下文、文件关联、代码库理解 |
| **用户交互记忆** | 对话风格、响应偏好、反馈学习 |
| **技能记忆** | 已安装技能、配置参数、使用频率 |

## 团队

| 角色 | 人员 |
|------|------|
| **项目负责人** | 唐锋（燧弘华创 执行总裁） |
| **架构设计** | 爱马仕系统 |
| **后端开发** | 主会话开发模式 |

## 许可证

Copyright © 2026 燧弘华创科技有限公司

---

*创建时间：2026 年 4 月 10 日*  
*版本：v0.2.0*  
*状态：OpenClaw Integration In Progress*
