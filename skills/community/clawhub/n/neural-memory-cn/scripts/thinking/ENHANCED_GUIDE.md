# 神经记忆系统增强版使用说明

## 新增组件

### 1. 意图理解层 (IntentUnderstandingLayer)
**核心功能**: 思考判断逻辑模块
- 分析用户查询意图
- 提取关键概念
- 判断与哪些神经元记忆相关
- 返回相关性排序的神经元列表

**使用示例**:
`python
from thinking import ThinkingModule

# 初始化增强版
module = ThinkingModule()
module.initialize_from_existing_memory()

# 智能思考（自动分析意图）
result = module.think("最近中医学得怎么样？", mode='smart')

# 查看结果
print(f"意图类型: {result['analysis']['intent_type']}")
print(f"相关概念: {result['analysis']['concepts']}")
print(f"激活的记忆: {[r['neuron'].name for r in result['results']]}")
`

### 2. 语义相似度引擎 (SemanticSimilarityEngine)
**核心功能**: 真正的语义匹配
- 支持嵌入向量计算
- 本地降级模式（关键词相似度）
- 自动缓存嵌入结果

### 3. 按需加载机制 (LazyStorageManager)
**核心功能**: 降低上下文长度
- L1 热缓存：最近激活的神经元
- L2 索引：所有神经元的元数据
- L3 文件存储：完整神经元数据

**快速获取相关记忆**:
`python
# 只获取与查询相关的记忆（用于构建上下文）
memories = module.get_relevant_memories("民航安全", top_k=5)
for m in memories:
    print(f"{m['name']}: 相关度 {m['relevance']:.2f}")
`

## 思考模式

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| smart | 智能模式，自动分析意图 | 默认推荐，自然语言查询 |
| exact | 精确模式，按名称匹配 | 已知确切概念名称 |
| ssociative | 联想模式，从匹配神经元扩散 | 探索关联知识 |

## 学习新知识

`python
# 学习新概念（自动建立关联）
module.learn_and_think(
    content="AI辅助舌诊的技术难点包括数据标注、光照校正...",
    concept_name="AI舌诊",
    concept_type="topic",
    tags=["中医", "AI", "诊断"]
)
`

## 配置选项

编辑 config.yaml:

`yaml
thinking:
  mode: "smart"  # 默认思考模式
  
  enhanced:
    use_intent_layer: true      # 启用意图理解
    use_semantic_engine: true   # 启用语义相似度
    use_lazy_loading: true      # 启用按需加载
  
  intent:
    relevance_threshold: 0.4    # 相关性阈值
    max_related_neurons: 10     # 最多返回数量
`

## 文件结构

`
thinking/
├── __init__.py           # 主入口（自动选择增强版/基础版）
├── enhanced_init.py      # 增强版主模块
├── config.yaml           # 配置文件
├── core/
│   ├── models.py         # 神经元、突观数据模型
│   ├── engine.py         # 激活扩散引擎
│   ├── intent/           # 新增：意图理解模块
│   │   ├── intent_layer.py       # 意图理解层
│   │   ├── semantic_engine.py    # 语义相似度引擎
│   │   └── related_neuron.py     # 相关神经元模型
│   └── ...
└── storage/
    ├── manager.py        # 原有存储管理器
    └── lazy_manager.py   # 新增：按需加载存储管理器
`

## 与 OpenClaw 集成

增强版模块会自动与 OpenClaw 的记忆系统集成：

1. **查询时**: 使用 get_relevant_memories() 只加载相关记忆
2. **学习时**: 自动建立知识关联
3. **思考时**: 意图分析 + 激活扩散

## 性能优化

- 热缓存默认 100 个神经元
- 语义嵌入结果自动缓存
- 索引只存储元数据，不存储完整内容
