# Neural Memory API Reference / 神经记忆 API 参考

## ThinkingModule / 思维模块

**English**: Main entry point for the neural memory system.

**中文**: 神经记忆系统的主入口点。

### Constructor / 构造函数

```python
ThinkingModule(base_path: str = "~/.neural-memory", config: Dict = None)
```

**Parameters / 参数**:
- `base_path`: Directory for storing memory data / 存储记忆数据的目录
- `config`: Optional configuration dictionary / 可选的配置字典

---

### Methods / 方法

#### think() / 思考

```python
think(query: str, mode: str = 'smart', max_depth: int = None) -> Dict
```

**English**: Query the memory system.

**中文**: 查询记忆系统。

**Parameters / 参数**:
- `query`: User's query string / 用户的查询字符串
- `mode`: One of 'smart', 'exact', 'associative' / 模式：'smart'、'exact'、'associative'
- `max_depth`: Maximum depth for activation spreading / 激活扩散的最大深度

**Returns / 返回值**:
```python
{
    'query': str,                    # Original query / 原始查询
    'analysis': {                    # Intent analysis (smart mode only) / 意图分析（仅智能模式）
        'intent_type': str,          # question, statement, request, unknown
        'concepts': List[str],       # Extracted concepts / 提取的概念
        'related_count': int         # Number of related neurons found / 找到的相关神经元数量
    },
    'results': [                     # Activated neurons / 激活的神经元
        {
            'neuron': Neuron,        # The neuron object / 神经元对象
            'activation': float      # Activation value / 激活值
        }
    ],
    'stats': {
        'total_activated': int,      # Total neurons activated / 总激活神经元数
        'seeds_used': int            # Number of seed neurons / 种子神经元数量
    }
}
```

**Error Returns / 错误返回**:
```python
{'query': str, 'error': 'empty_query'}        # Empty query / 空查询
{'query': str, 'error': 'concept_not_found'}  # Concept not found / 概念未找到
{'query': str, 'error': 'no_related_neurons'} # No related neurons / 无相关神经元
```

---

#### learn_and_think() / 学习并思考

```python
learn_and_think(
    content: str,
    concept_name: str,
    concept_type: str = 'concept',
    tags: List[str] = None,
    use_llm: bool = True
) -> Dict
```

**English**: Learn new knowledge and trigger thinking.

**中文**: 学习新知识并触发思考。

**Parameters / 参数**:
- `content`: Detailed content of the knowledge / 知识的详细内容
- `concept_name`: Name for the neuron / 神经元名称
- `concept_type`: Type of neuron (concept, fact, experience, preference) / 神经元类型
- `tags`: List of tags for categorization / 分类标签列表
- `use_llm`: Whether to use LLM for concept extraction / 是否使用LLM提取概念

**Returns / 返回值**:
```python
{
    'neuron': Neuron,               # Created/updated neuron / 创建/更新的神经元
    'connections_created': int,     # Number of new connections / 新连接数量
    'thinking_result': Dict         # Result of thinking on new concept / 新概念思考结果
}
```

---

#### get_relevant_memories() / 获取相关记忆

```python
get_relevant_memories(query: str, top_k: int = 5) -> List[Dict]
```

**English**: Get relevant memories without full activation spreading.

**中文**: 获取相关记忆，无需完整激活扩散。

**Returns / 返回值**:
```python
[
    {
        'name': str,
        'type': str,
        'content': str,             # Truncated to 500 chars / 截断至500字符
        'relevance': float,         # Relevance score / 相关性分数
        'tags': List[str]
    }
]
```

---

#### get_thinking_stats() / 获取思考统计

```python
get_thinking_stats() -> Dict
```

**English**: Get statistics about the memory system.

**中文**: 获取记忆系统的统计信息。

**Returns / 返回值**:
```python
{
    'neurons_count': int,           # Total neurons / 神经元总数
    'synapses_count': int,          # Total synapses / 突触总数
    'protected_neurons_count': int, # Protected neurons / 受保护神经元数
    'thinking_sessions': int,       # Total think() calls / think()调用总数
    'total_activations': int,       # Total neurons activated / 总激活神经元数
    'hot_cache_size': int,          # Current hot cache size / 当前热缓存大小
    'semantic_indexed': int         # Neurons with embeddings / 有嵌入的神经元数
}
```

---

#### save() / 保存

```python
save() -> None
```

**English**: Save all memory data to disk.

**中文**: 将所有记忆数据保存到磁盘。

---

## Neuron Model / 神经元模型

```python
@dataclass
class Neuron:
    id: str                         # UUID
    name: str                       # Concept name / 概念名称
    type: str                       # concept, fact, experience, preference
    content: str                    # Detailed content / 详细内容
    tags: List[str]                 # Tags for categorization / 分类标签
    activationCount: int            # Times activated / 激活次数
    lastActivated: str              # ISO timestamp / ISO时间戳
    createdAt: str                  # ISO timestamp / ISO时间戳
    metadata: Dict                  # Additional metadata / 额外元数据

    def activate(self):
        """Increment activation count and update timestamp.
        增加激活次数并更新时间戳。"""

    @classmethod
    def create(cls, name, content, neuron_type, tags) -> 'Neuron':
        """Create a new neuron. 创建新神经元。"""

    @classmethod
    def from_dict(cls, data: Dict) -> 'Neuron':
        """Create from dictionary. 从字典创建。"""

    def to_dict(self) -> Dict:
        """Convert to dictionary. 转换为字典。"""
```

---

## Synapse Model / 突触模型

```python
@dataclass
class Synapse:
    id: str                         # UUID
    fromNeuron: str                 # Source neuron ID / 源神经元ID
    toNeuron: str                   # Target neuron ID / 目标神经元ID
    type: str                       # domain_related, shared_tag, similarity
    weight: float                   # 0.0 to 1.0 / 权重
    confidence: float               # 0.0 to 1.0 / 置信度
    createdBy: str                  # auto, user, reasoning, domain_definition
    createdAt: str                  # ISO timestamp / ISO时间戳
    lastReinforced: str             # ISO timestamp (optional) / 最后强化时间
    reinforcementCount: int         # Times reinforced / 强化次数
    metadata: Dict                  # Additional metadata / 额外元数据

    def reinforce(self, delta: float = 0.1):
        """Strengthen the connection. 增强连接。"""

    def decay(self, factor: float = 0.95):
        """Weaken the connection. 减弱连接。"""

    @classmethod
    def create(cls, from_id, to_id, synapse_type, weight, confidence) -> 'Synapse':
        """Create a new synapse. 创建新突触。"""

    @classmethod
    def from_dict(cls, data: Dict) -> 'Synapse':
        """Create from dictionary. 从字典创建。"""
```

---

## IntentUnderstandingLayer / 意图理解层

**English**: Analyzes queries to determine intent and find relevant neurons.

**中文**: 分析查询以确定意图并找到相关神经元。

### analyze_query() / 分析查询

```python
analyze_query(user_query: str, use_llm: bool = None) -> QueryAnalysis
```

**Returns / 返回值**:
```python
@dataclass
class QueryAnalysis:
    original_query: str
    extracted_concepts: List[str]
    intent_type: str                # question, statement, request, unknown
    related_neurons: List[RelatedNeuron]
    suggested_depth: int            # Recommended spreading depth / 建议扩散深度
```

---

## LazyStorageManager / 惰性存储管理器

**English**: Three-tier storage with LRU cache for on-demand loading.

**中文**: 三层存储，带LRU缓存用于按需加载。

### Tiers / 存储层级

1. **L1 - Hot Cache / 热缓存**: In-memory LRU cache for frequently accessed neurons
2. **L2 - Neuron Index / 神经元索引**: Lightweight metadata index for fast lookups
3. **L3 - File Storage / 文件存储**: Persistent JSON files

### Methods / 方法

```python
get_neuron(neuron_id: str) -> Optional[Neuron]
get_neuron_by_name(name: str) -> List[Neuron]
get_all_neurons() -> List[Neuron]
get_synapses_from(neuron_id: str) -> List[Synapse]
get_synapses_to(neuron_id: str) -> List[Synapse]
add_neuron(neuron: Neuron) -> bool
update_neuron(neuron_id: str, **kwargs) -> bool
delete_neuron(neuron_id: str) -> bool
get_protected_neurons() -> List[Neuron]
save_all() -> None
```

---

## ActivationSpreadingEngine / 激活扩散引擎

**English**: Implements activation spreading algorithm.

**中文**: 实现激活扩散算法。

### spread() / 扩散

```python
spread(
    query_neuron_id: str,
    max_depth: int = 3,
    decay_factor: float = 0.8,
    min_activation: float = 0.15,
    limit: int = 20
) -> Dict
```

**Algorithm / 算法**:

1. Start with query neuron at activation 1.0 / 从查询神经元开始，激活值为1.0
2. Spread to connected neurons through synapses / 通过突触扩散到连接的神经元
3. Apply decay factor at each depth level / 在每个深度层级应用衰减因子
4. Multiply by synapse weight / 乘以突触权重
5. Accumulate activations / 累积激活值
6. Filter by minimum activation threshold / 按最小激活阈值过滤
7. Return top results / 返回顶部结果

**Returns / 返回值**:
```python
{
    'results': [
        {'neuron': Neuron, 'activation': float}
    ],
    'stats': {
        'total_activated': int,
        'max_depth_reached': int,
        'returned': int
    }
}
```

---

## Configuration Schema / 配置模式

```yaml
thinking:
  enabled: bool
  mode: str                      # smart, exact, associative

  enhanced:
    use_intent_layer: bool
    use_semantic_engine: bool
    use_lazy_loading: bool
    use_llm_analysis: bool

  intent:
    use_llm: bool
    llm_base_url: str
    llm_model: str
    llm_api_key: str
    relevance_threshold: float   # 0.0-1.0
    max_related_neurons: int

  semantic:
    embedding_model: str
    cache_dir: str

  storage:
    hot_cache_size: int
    lazy_loading: bool

  parameters:
    default_max_depth: int       # 1-5
    decay_factor: float          # 0.5-0.9
    min_activation: float        # 0.0-0.5
    result_limit: int

  protection:
    enabled: bool
    protected_types: List[str]
    allow_update_protected: bool
    allow_delete_protected: bool
```