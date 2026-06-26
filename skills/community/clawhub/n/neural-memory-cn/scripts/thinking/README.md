# OpenClaw 思考模块使用指南

## 概述

思考模块是一个模拟人类神经网络突触机制的认知增强系统，用于建立知识之间的深度连接，实现快速联想和精准回忆。

## 核心特性

- **神经元系统**：每个知识概念、主题、洞察都是一个神经元
- **突触连接**：神经元之间通过突触连接，模拟神经信号传递
- **激活扩散**：查询概念时，激活信号沿突触传播到相关概念
- **强连接机制**：高频使用的连接会强化，形成记忆"高速路"
- **受保护属性**：用户身份、偏好、性格等核心属性不会被删除或衰减

## 文件结构

```
thinking/
├── __init__.py           # 主模块入口（ThinkingModule）
├── adapter.py            # OpenClaw 接口适配器
├── config.yaml           # 配置文件
├── core/
│   ├── models.py         # 数据模型（Neuron, Synapse）
│   ├── engine.py         # 激活扩散引擎
│   ├── synapse_manager.py  # 突触管理器
│   └── neuron_builder.py # 神经元构建器
└── storage/
    └── manager.py        # 存储管理器
```

## 快速开始

### 1. 初始化（首次使用）

```python
from thinking import ThinkingModule

# 创建思考模块实例（自动检测存储路径）
thinking = ThinkingModule()

# 或者指定自定义路径
# thinking = ThinkingModule(base_path="/path/to/your/storage")

# 从现有记忆文件初始化
thinking.initialize_from_existing_memory()

# 保存状态
thinking.save()
```

### 2. 基本使用

#### 思考一个概念
```python
result = thinking.think("中医")
print(f"激活了 {result['stats']['total_activated']} 个神经元")
for r in result['results'][:5]:
    print(f"  • {r['neuron'].name} ({r['activation']:.3f})")
```

#### 学习新内容并思考
```python
result = thinking.learn_and_think(
    content="五行学说包括金木水火土，它们之间存在相生相克关系",
    concept_name="五行学说",
    concept_type="topic",
    tags=["中医", "基础理论"]
)
```

#### 使用不同思考模式
```python
# 联想模式（默认）- 激活所有类型的连接
thinking.think("民航", mode='associative')

# 专注模式 - 仅相似概念
thinking.think("民航", mode='focused')

# 探索模式 - 所有连接（包括因果、类比等）
thinking.think("民航", mode='exploratory')
```

### 3. 集成到 OpenClaw

思考模块已经自动集成到以下方面：

#### 增强的记忆搜索
`memory_search` 接口已增强，会同时返回：
- 原始语义搜索结果
- 思考模块产生的联想结果（基于激活扩散）

#### 心跳自主学习
心跳检查时会自动运行思考模块：
1. 学习新内容
2. 建立知识连接
3. 执行思考分析
4. 记录思考结果到长期记忆

#### 学习流程集成
```python
from thinking.adapter import get_thinking_adapter

adapter = get_thinking_adapter()

# 学习新主题后自动思考
result = adapter.learn_and_think(
    content="eVTOL（电动垂直起降飞行器）是未来城市空中交通的主要载体",
    concept_name="eVTOL",
    concept_type="topic"
)

# 查看统计
stats = adapter.get_stats()
print(f"神经元数: {stats['neurons_count']}")
print(f"突触数: {stats['synapses_count']}")
```

## 概念类型

- `concept`: 一般概念（如"民航"、"金融"）
- `topic`: 学习主题（如"五行学说"、"系统动力学"）
- `insight`: 关键洞察（跨领域连接）
- `preference`: 个人偏好（受保护）
- `personality`: 性格特征（受保护）
- `identity`: 身份信息（受保护）
- `user_profile`: 用户档案（受保护）
- `user_preference`: 用户偏好（受保护）

## 突触类型

- `similarity`: 相似关系
- `causality`: 因果关系
- `opposition`: 对立关系
- `example`: 示例关系
- `analogy`: 类比关系
- `citation`: 引用关系

## 保护机制

用户的个人属性（`IDENTITY.md`, `USER.md`, `Preferences.md` 中的内容）对应的神经元受到保护：

- ✅ 允许：内容更新、激活、查询
- ❌ 禁止：删除、衰减（权重不会随时间降低）
- ⚠️ 谨慎：从受保护神经元出发的突触需要仔细评估

这确保了您的身份、偏好、性格等核心信息在长期学习中保持不变。

## 维护任务

### 自动维护
配置中设置了定期维护：
- 每隔30天衰减一次未激活的突触（保护的不衰减）
- 修剪低置信度突触（置信度<0.3）
- 保护突触不受影响

### 手动维护
```python
adapter.run_maintenance()
```

## 存储格式

### 神经元存储
`memory_long_term/neurons.json`
```json
{
  "neurons": [
    {
      "id": "uuid",
      "type": "concept",
      "name": "中医",
      "content": "...",
      "tags": ["中医", "基础理论"],
      "createdAt": "2026-03-15T03:00:00",
      "lastActivated": "2026-03-15T04:30:00",
      "activationCount": 15,
      "metadata": {}
    }
  ]
}
```

### 突触存储
`memory_long_term/synapses/{neuron_id}.json`
每个文件存储从一个神经元出发的所有突触。

### 激活日志
`memory_long_term/activation_logs/YYYY-MM-DD.json`
记录每天的激活查询历史，用于分析和优化。

## 配置调整

编辑 `thinking/config.yaml` 调整参数：

```yaml
thinking:
  parameters:
    default_max_depth: 3        # 最大传播深度
    decay_factor: 0.8           # 每步衰减因子
    min_activation: 0.15        # 最小激活阈值
    result_limit: 20            # 默认返回结果数

  protection:
    protected_types: [...]       # 受保护的类型列表
    allow_update_protected: true # 是否允许更新受保护内容
```

## 高级特性（待实现）

- 嵌入模型语义相似度计算（当前使用简单文本匹配）
- 激活路径可视化
- 突触置信度预测
- 多模态连接（图像、音频）
- 思考过程可解释性报告

## 故障排除

### 问题：思考模块未激活
- 检查 `initialize_from_existing_memory()` 是否已调用
- 查看 `memory_long_term/neurons.json` 是否存在

### 问题：联想结果不相关
- 增加 `max_depth` 获取更广关联
- 调整 `decay_factor` 改变传播衰减
- 创建更多显式突触连接

### 问题：个人属性被删除
- 检查 `protected_types` 配置
- 确保 `IDENTITY.md`, `USER.md` 对应的神经元类型正确

## 开发者信息

### 核心类
- `ThinkingModule`: 主模块
- `StorageManager`: 数据持久化
- `ActivationSpreadingEngine`: 激活扩散算法
- `SynapseManager`: 突触生命周期管理
- `NeuronBuilder`: 神经元构建
- `ThinkingAdapter`: OpenClaw 接口适配

### 扩展点
- 实现嵌入模型：重写 `_simple_similarity` 或集成 `sentence-transformers`
- 自定义突触类型：扩展 `Synapse.type` 枚举
- 新的思考模式：扩展 `ThinkingModule.think()` 模式参数

## 版本历史

- v0.1 (2026-03-15): 初始实现
  - 基础神经元/突触模型
  - 激活扩散引擎
  - 与现有记忆系统集成
  - 保护机制

## 下一步

1. ✅ 设计完成
2. 🚧 实现基础框架（进行中）
3. ⏳ 集成嵌入模型提升相似度计算
4. ⏳ 实现可视化工具
5. ⏳ 优化性能（缓存、异步）
