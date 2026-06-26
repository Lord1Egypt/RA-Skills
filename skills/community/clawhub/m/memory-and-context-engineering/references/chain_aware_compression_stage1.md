# 链感知上下文压缩 - 阶段1实施文档

## 概述

本文档记录了链感知上下文压缩的阶段1实施：链元数据增强。

## 背景

在上下文压缩过程中，链信息（因果链、逻辑链、操作链等）包含了高价值的认知结构。传统的压缩机制将链作为普通文本处理，可能导致关键逻辑断裂。

**问题示例**：
```
假设因果链分布在3个上下文块中：
- 块1：问题A（优先级高）
- 块2：原因B（优先级中）
- 块3：解决方案C（优先级高）

按优先级压缩后可能只保留：
- 块1：问题A
- 块3：解决方案C

结果：用户看到问题A→解决方案C，但缺少原因B！
```

## 阶段1目标

**链元数据增强**：在现有压缩机制中增强链信息的权重

### 实施内容

1. **扩展ContextBlock元数据**
   - 添加`chain_links`字段：记录包含的链ID列表
   - 添加`chain_types`字段：记录包含的链类型列表

2. **新增压缩策略**
   - 添加`CHAIN_AWARE`压缩策略
   - 为每种链类型分配权重
   - 基于链数量和类型提升优先级

3. **链类型权重配置**
   - 因果链（causal）：40
   - 逻辑链（logic）：35
   - 操作链（operation）：35
   - 叙事链（narrative）：30
   - 时间链（time）：25

4. **向后兼容**
   - 支持metadata中的旧式链标记
   - 不破坏现有压缩逻辑

## 实施细节

### 1. ContextBlock扩展

```python
class ContextBlock(BaseModel):
    # ... 原有字段 ...

    # 链元数据（链感知压缩支持）
    chain_links: list[str] = Field(
        default_factory=list,
        description="包含的链ID列表（用于链完整性保持）"
    )
    chain_types: list[str] = Field(
        default_factory=list,
        description="包含的链类型列表（用于链价值评估）"
    )
```

**使用示例**：
```python
block = ContextBlock(
    source=ContextSource.SHORT_TERM_MEMORY,
    priority=ContextPriority.HIGH,
    content="问题A→原因B→方案C",
    token_count=100,
    chain_links=["chain_001"],
    chain_types=["causal"]
)
```

### 2. 新增压缩策略

```python
class CompressionStrategy(str, Enum):
    # ... 原有策略 ...

    CHAIN_AWARE = "chain_aware"  # 链感知压缩（优先保留链信息）
```

### 3. 链感知排序算法

```python
def _sort_by_chain_aware(self, blocks: list[ContextBlock]) -> list[ContextBlock]:
    """链感知排序（优先保留包含链信息的块）"""

    def chain_aware_score(block: ContextBlock) -> float:
        """计算链感知评分"""
        score = 0.0

        # 1. 基础优先级权重
        score += self.PRIORITY_WEIGHTS.get(block.priority, 0) * 10

        # 2. 链类型权重（累加所有链类型的权重）
        for chain_type in block.chain_types:
            score += self._chain_type_weights.get(chain_type, 0)

        # 3. 链数量奖励（跨块链）
        score += len(block.chain_links) * 15

        # 4. 相关性和新鲜度作为辅助因素
        score += block.relevance_score * 10
        score += block.freshness_score * 10

        # 5. 向后兼容：检查metadata中的旧式链标记
        if "causal_chain" in block.metadata:
            score += 30
            # ...

        return score

    return sorted(blocks, key=lambda b: (chain_aware_score(b), -b.token_count), reverse=True)
```

### 4. 权重配置接口

```python
compressor.set_chain_type_weights({
    "causal": 50,
    "operation": 45
})
```

## 使用示例

### 基本使用

```python
from scripts.context_orchestrator import (
    ContextBlock,
    ContextCompressor,
    CompressionStrategy,
    ContextPriority,
    ContextSource
)

# 创建压缩器
compressor = ContextCompressor(
    default_strategy=CompressionStrategy.CHAIN_AWARE
)

# 创建包含链的上下文块
blocks = [
    ContextBlock(
        source=ContextSource.SHORT_TERM_MEMORY,
        priority=ContextPriority.MEDIUM,
        content="问题A→原因B→方案C",
        token_count=80,
        chain_links=["chain_001"],
        chain_types=["causal"]
    ),
    ContextBlock(
        source=ContextSource.SHORT_TERM_MEMORY,
        priority=ContextPriority.MEDIUM,
        content="步骤1→步骤2→结果",
        token_count=70,
        chain_links=["chain_002"],
        chain_types=["operation"]
    ),
    # ... 其他块
]

# 执行链感知压缩
result = compressor.compress(
    blocks=blocks,
    compression_ratio=0.5,
    strategy=CompressionStrategy.CHAIN_AWARE
)

print(f"原始Token数: {result.original_token_count}")
print(f"压缩后Token数: {result.compressed_token_count}")
print(f"保留的链块数: {len([b for b in result.compressed_blocks if b.chain_links])}")
```

### 集成到双轨架构

```python
from scripts.fusion import BucketChainFusion
from scripts.context_orchestrator import ContextCompressor

# 假设从双轨融合层获得结果
fusion_result = fusion.process(...)

# 将链信息附加到上下文块
blocks = []
for chain_id, chain in fusion_result.extracted_chains.items():
    block = ContextBlock(
        source=ContextSource.SHORT_TERM_MEMORY,
        priority=ContextPriority.HIGH,
        content=chain.content,
        token_count=len(chain.content.split()),
        chain_links=[chain_id],
        chain_types=[chain.chain_type.value]
    )
    blocks.append(block)

# 执行链感知压缩
compressor = ContextCompressor()
result = compressor.compress(
    blocks=blocks,
    compression_ratio=0.6,
    strategy=CompressionStrategy.CHAIN_AWARE
)
```

## 测试覆盖

已实现的单元测试：

1. **test_chain_metadata_in_context_block**
   - 验证ContextBlock中的链元数据字段

2. **test_chain_type_weights_configurable**
   - 验证链类型权重可配置

3. **test_chain_aware_sorting_priority**
   - 验证链感知排序优先级
   - 包含多条链的块应该排在第一位

4. **test_chain_aware_compression_preserves_chains**
   - 验证链感知压缩保留链信息
   - 链块应该被优先保留

5. **test_chain_aware_vs_priority_strategy**
   - 对比链感知策略和优先级策略
   - 验证链感知策略的优势

6. **test_backward_compatibility_with_metadata_chains**
   - 测试向后兼容（metadata中的旧式链标记）

7. **test_chain_aware_score_calculation**
   - 测试链感知评分计算细节

运行测试：
```bash
python -m pytest tests/test_chain_aware_compression.py -v
```

## 预期收益

1. **提升链压缩质量30-50%**
   - 链块优先级显著提升
   - 避免关键逻辑链断裂

2. **代码改动小**
   - 新增约100行代码
   - 不修改现有压缩逻辑

3. **风险低**
   - 向后兼容
   - 不破坏现有功能

4. **可扩展**
   - 为阶段2（链完整性保持）打下基础
   - 支持自定义链类型权重

## 链类型权重说明

| 链类型 | 权重 | 典型场景 | 说明 |
|--------|------|---------|------|
| **causal** | 40 | 调试 | 问题→原因→解决方案，逻辑完整性强 |
| **logic** | 35 | 分析 | 前提→推理→结论，严密逻辑推导 |
| **operation** | 35 | 编码 | 步骤1→步骤2→结果，操作序列 |
| **narrative** | 30 | 学习 | 事件A→事件B→事件C，叙事结构 |
| **time** | 25 | 历史追踪 | 时间1→时间2→时间3，时间线 |

## 评分公式

链感知评分 = 基础优先级 + 链类型权重 + 链数量奖励 + 相关性 + 新鲜度

其中：
- **基础优先级**：`PRIORITY_WEIGHTS[priority] * 10`
- **链类型权重**：`sum(WEIGHTS[type] for type in chain_types)`
- **链数量奖励**：`len(chain_links) * 15`
- **相关性**：`relevance_score * 10`
- **新鲜度**：`freshness_score * 10`

**示例计算**：
```
假设一个块：
- 优先级：HIGH (4.0)
- 链类型：["causal", "logic"]
- 链数量：2
- 相关性：0.8
- 新鲜度：0.9

评分 = 4.0 * 10 + (40 + 35) + 2 * 15 + 0.8 * 10 + 0.9 * 10
     = 40 + 75 + 30 + 8 + 9
     = 162
```

## 局限性

阶段1实施存在的限制：

1. **不保证链完整性**
   - 仍然可能切断跨块链
   - 只是提升了链块的保留概率

2. **静态权重**
   - 链类型权重固定
   - 不适应不同任务场景

3. **无链摘要**
   - 无法生成链的紧凑表示
   - 只能保留或删除整个块

## 下一步（阶段2）

阶段2：链完整性保持

- 识别跨块链，记录链节点-块的映射
- 压缩时采用"全保留或全移除"策略
- 利用MultiDimensionSummary生成链摘要

## 参考

- [context_compaction_rules.md](context_compaction_rules.md) - 上下文压缩规则
- [dual_track_architecture_overview.md](dual_track_architecture_overview.md) - 双轨架构总览
- [dual_track_module_design.md](dual_track_module_design.md) - 模块设计
