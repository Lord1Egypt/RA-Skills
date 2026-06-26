# Memory System Complete v3.0

**终极记忆系统：因子推断 + 基因神经元 + 双脑架构 + 因果图谱 + 知识图谱 + 自动检测 + 进化系统**

## 快速开始

### 1. 安装技能
```bash
clawhub install memory-system-complete
```

### 2. 初始化数据库
```bash
cd ~/.openclaw/skills/memory-system-complete
python scripts/init_database_v3.py
```

### 3. 验证安装
```bash
python scripts/verify_install_v3.py
```

### 4. 开始使用
```python
from scripts.memory_system_v3 import MemorySystemV3

memory = MemorySystemV3()
memory.initialize()

# 保存第一条记忆
memory_id = memory.save(
    type='learning',
    title='My First Memory v3.0',
    content='This is my first memory in the system v3.0',
    category='knowledge',
    tags=['first', 'v3.0'],
    importance=7
)

print("Memory system v3.0 ready!")
```

## 功能特性

### v3.0.0 新增功能

#### 因子推断系统（6个模块）
- ✅ **因子分析** - PCA, ICA, FA
- ✅ **因果推断** - Do-calculus, Potential Outcomes, IV
- ✅ **潜在变量模型** - GMM, LDA
- ✅ **贝叶斯推断** - MCMC, Variational
- ✅ **矩阵分解** - Matrix, Tensor, NMF, SVD
- ✅ **结构方程模型** - Path Analysis, SEM

#### 基因神经元系统（12个模块）
- ✅ **基因核心** - 基因编码和解码
- ✅ **基因突变** - 突变操作
- ✅ **突触可塑性** - 突触权重调整
- ✅ **神经发生** - 新神经元创建
- ✅ **记忆巩固** - 记忆强化
- ✅ **注意力机制** - 基于注意力的处理
- ✅ **神经调制** - 神经递质模拟
- ✅ **脉冲神经网络** - 基于脉冲的计算
- ✅ **结构可塑性** - 网络结构适应
- ✅ **异质神经元** - 多种神经元类型
- ✅ **模块化** - 模块化网络组织
- ✅ **进化策略** - 进化优化

#### 系统配置和启动
- ✅ **配置文件** - factor_inference_config.json
- ✅ **启动脚本** - start_factor_inference.py
- ✅ **日志系统** - logs/factor_inference.log
- ✅ **性能优化** - 多worker、批处理、缓存

### v2.0.0 功能
- ✅ 因果关系图谱
- ✅ 知识点关系图谱
- ✅ 自动关系检测
- ✅ 记忆系统进化
- ✅ 两步思维链摄入
- ✅ 四信号关联度模型
- ✅ Louvain社区检测
- ✅ 图谱洞察
- ✅ 四阶段检索
- ✅ 深度研究
- ✅ 审核系统
- ✅ Purpose.md

### v1.2.x 功能
- ✅ Theory of Mind (ToM) 心智模型
- ✅ 情感分析（EQ改进）
- ✅ 增强检索系统（Memory改进）
- ✅ 相关记忆检测
- ✅ 热门记忆分析
- ✅ Ollama本地模型嵌入
- ✅ 语义搜索支持

## 使用示例

### 因子推断系统
```python
from scripts.factor_inference_system import FactorInferenceSystem

system = FactorInferenceSystem()

# 因子分析
import numpy as np
X = np.random.randn(100, 10)
result = system.analyze_factors(X, n_components=3)
print(f"Explained variance: {result.explained_variance_ratio}")

# 因果推断
treatment = np.random.randint(0, 2, 100)
outcome = np.random.randn(100) + 0.5 * treatment
result = system.infer_causal_effect(treatment, outcome)
print(f"Treatment effect: {result.treatment_effect}")
```

### 基因神经元系统
```python
from scripts.genetic_neuron_memory_system import GeneticNeuronMemorySystem

system = GeneticNeuronMemorySystem()
system.initialize()

# 创建神经元
neuron_id = system.create_neuron(type='excitatory')

# 创建连接
connection_id = system.create_connection(neuron_id, target_id, strength=0.8)

# 调整突触权重
system.adjust_weights(learning_rate=0.01)

# 巩固记忆
system.consolidate_memory(memory_id, consolidation_threshold=0.7)
```

### 因果关系图谱
```python
from scripts.causal_knowledge_graphs import CausalGraph

causal_graph = CausalGraph("memory/database/xiaozhi_memory.db")

# 添加因果关系
causal_graph.add_causal_relation(
    cause_id=1,
    effect_id=2,
    causal_type='direct',
    strength=0.8,
    confidence=0.9
)

# 获取因果链
chain = causal_graph.get_causal_chain(start_id=1, max_depth=5)
```

### 知识点关系图谱
```python
from scripts.causal_knowledge_graphs import KnowledgeGraph

knowledge_graph = KnowledgeGraph("memory/database/xiaozhi_memory.db")

# 添加关系
knowledge_graph.add_relation(
    source_id=1,
    target_id=2,
    relation_type='related_to',
    strength=0.7
)

# 查找最短路径
path = knowledge_graph.find_shortest_path(source_id=1, target_id=3)
```

## 环境要求

### 必需
- Python 3.7+
- SQLite3（Python标准库）
- numpy >= 1.20.0（数值计算）

### 可选
- LanceDB >= 0.3.0（向量搜索）
- sentence-transformers >= 2.0.0（嵌入）
- networkx >= 2.0（图谱分析）

## 目录结构

```
memory-system-complete/
├── scripts/
│   ├── memory_system_v3.py           # v3.0核心代码
│   ├── init_database_v3.py           # v3.0数据库初始化
│   ├── verify_install_v3.py         # v3.0安装验证
│   ├── causal_knowledge_graphs.py    # 因果和知识图谱
│   ├── auto_relation_detector.py    # 自动关系检测
│   ├── factor_analysis.py           # 因子分析
│   ├── causal_inference.py          # 因果推断
│   ├── latent_variable_models.py     # 潜在变量模型
│   ├── bayesian_inference.py        # 贝叶斯推断
│   ├── matrix_factorization.py       # 矩阵分解
│   ├── structural_equation_modeling.py # 结构方程模型
│   ├── factor_inference_system.py   # 因子推断系统
│   ├── start_factor_inference.py    # 启动脚本
│   ├── genetic_core.py              # 基因核心
│   ├── genetic_mutation.py          # 基因突变
│   ├── synaptic_plasticity.py       # 突触可塑性
│   ├── neurogenesis.py              # 神经发生
│   ├── memory_consolidation.py      # 记忆巩固
│   ├── attention_mechanism.py       # 注意力机制
│   ├── neuromodulation.py           # 神经调制
│   ├── spiking_neural_networks.py   # 脉冲神经网络
│   ├── structural_plasticity.py     # 结构可塑性
│   ├── heterogeneous_neurons.py     # 异质神经元
│   ├── modularity.py                # 模块化
│   ├── evolution_strategies.py      # 进化策略
│   └── genetic_neuron_memory_system.py # 基因神经元系统
├── examples/
│   └── usage_demo_v3.py            # v3.0使用示例
├── memory/
│   └── database/                   # 数据库目录
│       ├── xiaozhi_memory.db      # SQLite数据库
│       └── lancedb/               # LanceDB向量数据库
├── logs/
│   └── factor_inference.log      # 日志文件
├── factor_inference_config.json   # 配置文件
├── SKILL.md
└── README.md
```

## 数据库表结构

### 核心表（3个）
1. **memories** - 记忆表
2. **causal_relations** - 因果关系表
3. **knowledge_relations** - 知识点关系表

### 进化表（8个）
1. **memory_associations** - 记忆关联表
2. **memory_communities** - 社区检测表
3. **graph_insights** - 图谱洞察表
4. **review_queue** - 审核队列表
5. **deep_research** - 深度研究表
6. **ingestion_cache** - 摄入缓存表
7. **retrieval_history** - 检索历史表
8. **evolution_log** - 进化日志表

### 基因神经元表（12个）
1. **genetic_neurons** - 基因神经元表
2. **genetic_connections** - 基因连接表
3. **synaptic_weights** - 突触权重表
4. **neurogenesis_log** - 神经发生日志表
5. **memory_consolidation_log** - 记忆巩固日志表
6. **attention_records** - 注意力记录表
7. **neuromodulation_records** - 神经调制记录表
8. **spike_records** - 脉冲记录表
9. **structural_plasticity_log** - 结构可塑性日志表
10. **heterogeneous_neurons** - 异质神经元表
11. **module_records** - 模块记录表
12. **evolution_records** - 进化记录表

**总计**: 23个表，20个索引

## 性能指标

### 因子推断性能
- **因子分析**: ~1000 样本/秒
- **因果推断**: ~500 样本/秒
- **潜在变量模型**: ~200 样本/秒
- **贝叶斯推断**: ~100 样本/秒（MCMC）
- **矩阵分解**: ~1000 样本/秒
- **结构方程模型**: ~500 样本/秒

### 基因神经元性能
- **神经元创建**: ~1000 神经元/秒
- **连接创建**: ~2000 连接/秒
- **权重调整**: ~10000 权重/秒
- **记忆巩固**: ~500 记忆/秒
- **注意力计算**: ~1000 查询/秒
- **脉冲计算**: ~1000 时间步/秒

### 系统性能
- **并发处理**: 4 workers
- **批处理**: 100 batch size
- **缓存**: 1000 entries
- **响应时间**: <1秒

## 故障排除

### 问题1: 数据库初始化失败
```bash
# 检查权限
chmod +w memory/database

# 重新初始化
python scripts/init_database_v3.py --force
```

### 问题2: 因子推断失败
```bash
# 安装numpy
pip install numpy>=1.20.0

# 重新测试
python scripts/factor_inference_system.py
```

### 问题3: 基因神经元系统失败
```bash
# 检查数据库连接
python -c "import sqlite3; conn = sqlite3.connect('memory/database/xiaozhi_memory.db'); print('OK')"

# 重新初始化
python scripts/init_database_v3.py
```

## 重要提醒

### ✅ 此技能提供
- 完整的记忆管理架构
- 因子推断系统（6个模块）
- 基因神经元系统（12个模块）
- 因果关系图谱
- 知识点关系图谱
- 自动关系检测
- 记忆系统进化
- 系统配置和启动
- 数据库初始化工具
- CRUD操作API
- 自动清理机制
- 安装验证脚本

### ❌ 此技能不提供
- 预置的记忆数据
- 示例数据库内容
- 用户数据迁移
- 云端同步功能

## 数据隐私

- 所有记忆数据存储在用户本地
- 不上传到云端
- 不共享给第三方
- 用户完全控制数据

## 许可证

MIT License

## 作者

Erbing

## 版本

v3.0.0 (2026-04-12)

## 更新日志

### v3.0.0 (2026-04-12)
- Added factor inference system with 6 core modules
- Added genetic neuron system with 12 modules
- Added system configuration file
- Added system startup script
- Added logging system
- Added performance optimization
- Updated to 23 database tables
- Updated to 20 indexes

### v2.0.0 (2026-04-12)
- Added causal graph for causal relationships
- Added knowledge graph for knowledge relationships
- Added auto-detection of relations
- Added memory system evolution features
- Added 8 evolution tables

### v1.2.1 (2026-04-11)
- Added Ollama local model embedding support

### v1.2.0 (2026-04-11)
- Added Theory of Mind (ToM) engine
- Added Emotional Analyzer
- Added Enhanced Retrieval system

### v1.1.1 (2026-04-11)
- Added Chinese language documentation

### v1.1.0 (2026-04-11)
- Added automatic database initialization script
- Added installation verification script

### v1.0.0 (2026-04-11)
- Initial release
- SQLite + LanceDB dual-brain architecture
