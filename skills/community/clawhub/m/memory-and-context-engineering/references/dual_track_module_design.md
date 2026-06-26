# 双轨并行提炼架构（新增） - 模块详细设计

## 目录

1. [数据结构设计](#数据结构设计)
2. [接口定义](#接口定义)
3. [类图和时序图](#类图和时序图)
4. [关键算法说明](#关键算法说明)

---

## 数据结构设计

### 1. 链基类和派生类

#### BaseExtractedChain（基类）

```python
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field

class BaseExtractedChain(BaseModel, ABC):
    """
    提取链的基类
    
    所有链类型必须继承此类，实现统一的接口。
    """
    
    # 基础字段
    chain_id: str = Field(
        default_factory=lambda: f"chain_{uuid.uuid4().hex[:8]}",
        description="链唯一标识符"
    )
    chain_type: ChainType = Field(description="链类型")
    content: str = Field(description="原始文本内容")
    extraction_confidence: float = Field(
        ge=0.0,
        le=1.0,
        default=0.5,
        description="提取置信度"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="创建时间"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="扩展元数据"
    )
    
    @abstractmethod
    def to_summary(self) -> str:
        """生成摘要（子类必须实现）"""
        raise NotImplementedError
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典（用于序列化）"""
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BaseExtractedChain":
        """从字典创建实例"""
        return cls(**data)
```

#### ExtractedCausalChain（因果链）

```python
class ExtractedCausalChain(BaseExtractedChain):
    """
    因果链：问题→原因→解决方案
    
    用途：提取和表示因果关系
    """
    
    chain_type: ChainType = ChainType.CAUSAL
    
    # 因果节点
    problem: ProblemNode = Field(description="问题节点")
    causes: list[CauseNode] = Field(
        default_factory=list,
        description="原因节点列表"
    )
    causal_relations: list[CausalRelation] = Field(
        default_factory=list,
        description="因果关系列表"
    )
    solutions: list[SolutionNode] = Field(
        default_factory=list,
        description="解决方案列表"
    )
    
    # 源信息
    source_text: str = Field(
        default="",
        description="来源文本"
    )
    
    def to_summary(self) -> str:
        """生成因果链摘要"""
        lines = []
        
        # 问题
        lines.append(f"问题: {self.problem.content}")
        
        # 原因
        if self.causes:
            root_causes = [c for c in self.causes if c.is_root_cause]
            if root_causes:
                cause_text = ", ".join(c.content for c in root_causes)
            else:
                cause_text = ", ".join(c.content for c in self.causes)
            lines.append(f"原因: {cause_text}")
        
        # 解决方案
        if self.solutions:
            solution_text = ", ".join(s.content for s in self.solutions)
            lines.append(f"解决方案: {solution_text}")
        
        return "\n".join(lines)
```

#### ExtractedLogicChain（逻辑链）

```python
class ExtractedLogicChain(BaseExtractedChain):
    """
    逻辑链：前提→推理→结论
    
    用途：提取和表示推理过程
    """
    
    chain_type: ChainType = ChainType.LOGIC
    
    # 逻辑节点
    premises: list[str] = Field(
        default_factory=list,
        description="前提列表"
    )
    inference_steps: list[str] = Field(
        default_factory=list,
        description="推理步骤列表"
    )
    conclusion: str = Field(
        default="",
        description="结论"
    )
    
    # 逻辑类型
    logic_type: str = Field(
        default="deductive",
        description="逻辑类型：deductive/inductive/abductive"
    )
    
    def to_summary(self) -> str:
        """生成逻辑链摘要"""
        lines = []
        
        # 前提
        if self.premises:
            premises_text = ", ".join(self.premises)
            lines.append(f"前提: {premises_text}")
        
        # 推理
        if self.inference_steps:
            inference_text = " → ".join(self.inference_steps)
            lines.append(f"推理: {inference_text}")
        
        # 结论
        if self.conclusion:
            lines.append(f"结论: {self.conclusion}")
        
        return "\n".join(lines)
```

#### ExtractedOperationChain（操作链）

```python
class ExtractedOperationChain(BaseExtractedChain):
    """
    操作链：动作1→动作2→结果
    
    用途：提取和表示执行步骤
    """
    
    chain_type: ChainType = ChainType.OPERATION
    
    # 操作节点
    steps: list[str] = Field(
        default_factory=list,
        description="操作步骤列表"
    )
    expected_outcome: str = Field(
        default="",
        description="预期结果"
    )
    resources_needed: list[str] = Field(
        default_factory=list,
        description="所需资源列表"
    )
    
    # 操作属性
    estimated_duration: str = Field(
        default="",
        description="预估耗时"
    )
    
    def to_summary(self) -> str:
        """生成操作链摘要"""
        steps_str = " → ".join(self.steps)
        if self.expected_outcome:
            return f"操作链: {steps_str} → {self.expected_outcome}"
        return f"操作链: {steps_str}"
```

#### ExtractedNarrativeChain（叙事链）

```python
class ExtractedNarrativeChain(BaseExtractedChain):
    """
    叙事链：事件1→事件2→事件3
    
    用途：提取和表示叙事流程
    """
    
    chain_type: ChainType = ChainType.NARRATIVE
    
    # 叙事节点
    events: list[dict[str, Any]] = Field(
        default_factory=list,
        description="事件列表"
    )
    narrative_arc: str = Field(
        default="",
        description="叙事弧：intro/rising/climax/falling/resolution"
    )
    
    # 叙事属性
    protagonist: str = Field(
        default="",
        description="主角"
    )
    
    def to_summary(self) -> str:
        """生成叙事链摘要"""
        if not self.events:
            return "叙事链: 无事件"
        
        event_descriptions = [
            e.get("description", "") 
            for e in self.events
        ]
        events_str = " → ".join(event_descriptions)
        return f"叙事: {events_str}"
```

#### ExtractedTimeChain（时间链）

```python
class ExtractedTimeChain(BaseExtractedChain):
    """
    时间链：时间点A→时间点B→时间点C
    
    用途：提取和表示时序关系
    """
    
    chain_type: ChainType = ChainType.TIME
    
    # 时间节点
    timeline: list[dict[str, Any]] = Field(
        default_factory=list,
        description="时间线列表"
    )
    duration: str = Field(
        default="",
        description="总时长"
    )
    
    def to_summary(self) -> str:
        """生成时间链摘要"""
        if not self.timeline:
            return "时间线: 无时间点"
        
        time_str = " → ".join(
            f"{t['time']}: {t['event']}" 
            for t in self.timeline
        )
        return f"时间线: {time_str}"
```

### 2. 链缓冲区

```python
class ChainBuffer(BaseModel):
    """
    链缓冲区（独立的链存储空间）
    
    为每种链类型提供独立的缓冲区，支持TTL和容量管理。
    """
    
    buffer_id: str = Field(description="缓冲区ID")
    buffer_type: ChainType = Field(description="链类型")
    
    # 存储的链
    chains: list[BaseExtractedChain] = Field(
        default_factory=list,
        description="存储的链列表"
    )
    
    # 缓冲区配置
    max_capacity: int = Field(
        default=50,
        description="最大容量"
    )
    ttl_minutes: int = Field(
        default=30,
        description="过期时间（分钟）"
    )
    
    # 质量指标
    avg_confidence: float = Field(
        default=0.0,
        description="平均置信度"
    )
    completeness_score: float = Field(
        default=0.0,
        description="完整性评分"
    )
    
    # 元数据
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="创建时间"
    )
    last_accessed: datetime = Field(
        default_factory=datetime.now,
        description="最后访问时间"
    )
    
    def add_chain(self, chain: BaseExtractedChain) -> bool:
        """
        添加链到缓冲区
        
        Returns:
            是否添加成功
        """
        # 检查容量
        if len(self.chains) >= self.max_capacity:
            # 移除最旧的链（LRU）
            self.chains.pop(0)
        
        # 添加链
        self.chains.append(chain)
        self.last_accessed = datetime.now()
        
        # 更新统计
        self._update_statistics()
        
        return True
    
    def get_chains(self, limit: int | None = None) -> list[BaseExtractedChain]:
        """
        获取链
        
        Args:
            limit: 限制数量
        
        Returns:
            链列表
        """
        self.last_accessed = datetime.now()
        
        if limit is None:
            return self.chains
        
        return self.chains[-limit:]
    
    def cleanup_expired(self) -> int:
        """
        清理过期的链
        
        Returns:
            清理的数量
        """
        now = datetime.now()
        before_count = len(self.chains)
        
        # 移除过期链
        self.chains = [
            chain for chain in self.chains
            if (now - chain.created_at).total_seconds() < self.ttl_minutes * 60
        ]
        
        after_count = len(self.chains)
        return before_count - after_count
    
    def _update_statistics(self) -> None:
        """更新统计信息"""
        if not self.chains:
            self.avg_confidence = 0.0
            self.completeness_score = 0.0
            return
        
        # 平均置信度
        self.avg_confidence = sum(
            chain.extraction_confidence 
            for chain in self.chains
        ) / len(self.chains)
        
        # 完整性评分（简化计算）
        self.completeness_score = min(1.0, len(self.chains) / 10.0)
```

### 3. 话题簇

```python
class TopicCluster(BaseModel):
    """
    话题簇（语义桶的提炼结果）
    
    通过聚类算法将相似的记忆项聚合。
    """
    
    cluster_id: str = Field(description="簇ID")
    topic_label: str = Field(description="话题标签")
    dominant_bucket: SemanticBucketType = Field(description="主导桶类型")
    
    # 关键词
    keywords: set[str] = Field(default_factory=set)
    
    # 包含的记忆项
    items: list[ShortTermMemoryItem] = Field(default_factory=list)
    
    # 质量指标
    avg_relevance: float = Field(default=0.0)
    coherence: float = Field(default=0.0)
    priority: float = Field(default=0.0)
    
    # 关联信息
    related_chains: list[str] = Field(default_factory=list)
    extraction_candidate: bool = False
    
    # 元数据
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    
    def add_item(self, item: ShortTermMemoryItem) -> None:
        """添加记忆项"""
        self.items.append(item)
        self.last_updated = datetime.now()
        
        # 更新关键词
        item_keywords = extract_keywords(item.content)
        self.keywords.update(item_keywords)
        
        # 更新统计
        self._update_statistics()
    
    def _update_statistics(self) -> None:
        """更新统计信息"""
        if not self.items:
            self.avg_relevance = 0.0
            self.coherence = 0.0
            return
        
        # 平均相关性
        self.avg_relevance = sum(
            item.relevance_score 
            for item in self.items
        ) / len(self.items)
        
        # 内聚性（简化计算）
        self.coherence = calculate_coherence(self.items)
```

---

## 接口定义

### 1. 链提取器接口

```python
from abc import ABC, abstractmethod

class BaseChainExtractor(ABC):
    """
    链提取器基类
    
    所有链提取器必须实现此接口。
    """
    
    @abstractmethod
    def extract(
        self,
        text: str,
        context: dict[str, Any] | None = None
    ) -> list[BaseExtractedChain]:
        """
        从文本提取链
        
        Args:
            text: 输入文本
            context: 上下文信息（可选）
        
        Returns:
            提取的链列表
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_chain_type(self) -> ChainType:
        """返回链类型"""
        raise NotImplementedError
    
    def validate_input(self, text: str) -> bool:
        """
        验证输入文本
        
        Args:
            text: 输入文本
        
        Returns:
            是否有效
        """
        return len(text.strip()) > 0
```

### 2. 链存储管理器接口

```python
class ChainStorageManager(BaseModel):
    """
    链存储管理器接口
    
    提供统一的链存储和检索接口。
    """
    
    short_term: ShortTermMemoryManager
    
    def store_chain(
        self,
        chain: BaseExtractedChain,
        bucket_type: SemanticBucketType | None = None
    ) -> str:
        """
        存储链到短期记忆
        
        Args:
            chain: 链对象
            bucket_type: 语义桶类型（可选，自动推断）
        
        Returns:
            记忆项ID
        """
        # 自动推断桶类型
        if bucket_type is None:
            bucket_type = self._infer_bucket_type(chain.chain_type)
        
        # 序列化链数据
        chain_dict = chain.to_dict()
        
        # 存储到短期记忆
        item_id = self.short_term.store_with_semantics(
            content=chain.content,
            bucket_type=bucket_type,
            topic_label=f"{chain.chain_type.value}_chain",
            relevance_score=chain.extraction_confidence,
            metadata={
                "chain_type": chain.chain_type.value,
                "chain_data": chain_dict,
                "chain_id": chain.chain_id,
                "chain_summary": chain.to_summary()
            }
        )
        
        return item_id
    
    def retrieve_chains(
        self,
        chain_type: ChainType | None = None,
        bucket_type: SemanticBucketType | None = None,
        limit: int = 10
    ) -> list[BaseExtractedChain]:
        """
        检索链
        
        Args:
            chain_type: 链类型（可选）
            bucket_type: 语义桶类型（可选）
            limit: 返回数量
        
        Returns:
            链对象列表
        """
        chains = []
        
        for bucket in self.short_term.buckets.values():
            for item in bucket.items:
                # 过滤条件
                metadata = item.metadata
                
                if chain_type:
                    if metadata.get("chain_type") != chain_type.value:
                        continue
                
                if bucket_type:
                    if item.bucket_type != bucket_type:
                        continue
                
                # 反序列化链
                chain_data = metadata.get("chain_data")
                if chain_data:
                    chain = self._deserialize_chain(chain_data)
                    if chain:
                        chains.append(chain)
        
        return chains[:limit]
    
    def _infer_bucket_type(self, chain_type: ChainType) -> SemanticBucketType:
        """推断链类型对应的语义桶"""
        mapping = {
            ChainType.CAUSAL: SemanticBucketType.TASK_CONTEXT,
            ChainType.LOGIC: SemanticBucketType.DECISION_CONTEXT,
            ChainType.OPERATION: SemanticBucketType.TASK_CONTEXT,
            ChainType.NARRATIVE: SemanticBucketType.TASK_CONTEXT,
            ChainType.TIME: SemanticBucketType.TASK_CONTEXT,
        }
        return mapping.get(chain_type, SemanticBucketType.TASK_CONTEXT)
    
    def _deserialize_chain(self, data: dict[str, Any]) -> BaseExtractedChain | None:
        """反序列化链"""
        chain_type = data.get("chain_type")
        
        chain_classes = {
            ChainType.CAUSAL: ExtractedCausalChain,
            ChainType.LOGIC: ExtractedLogicChain,
            ChainType.OPERATION: ExtractedOperationChain,
            ChainType.NARRATIVE: ExtractedNarrativeChain,
            ChainType.TIME: ExtractedTimeChain,
        }
        
        chain_class = chain_classes.get(ChainType(chain_type))
        if chain_class:
            try:
                return chain_class(**data)
            except Exception:
                return None
        
        return None
```

### 3. 提取器编排器接口

```python
class ChainExtractorOrchestrator(BaseModel):
    """
    链提取器编排器
    
    管理所有链提取器，提供统一的提取接口。
    """
    
    extractors: dict[ChainType, BaseChainExtractor] = Field(
        default_factory=dict
    )
    
    def register_extractor(
        self,
        extractor: BaseChainExtractor
    ) -> None:
        """注册提取器"""
        chain_type = extractor.get_chain_type()
        self.extractors[chain_type] = extractor
    
    def extract_all_chains(
        self,
        text: str,
        context: dict[str, Any] | None = None
    ) -> dict[ChainType, list[BaseExtractedChain]]:
        """
        提取所有类型的链
        
        Args:
            text: 输入文本
            context: 上下文信息
        
        Returns:
            链类型到链列表的映射
        """
        results = {}
        
        for chain_type, extractor in self.extractors.items():
            try:
                results[chain_type] = extractor.extract(text, context)
            except Exception as e:
                # 记录错误，继续处理其他链类型
                print(f"Error extracting {chain_type}: {e}")
                results[chain_type] = []
        
        return results
    
    def extract_specific_chain(
        self,
        text: str,
        chain_type: ChainType,
        context: dict[str, Any] | None = None
    ) -> list[BaseExtractedChain]:
        """
        提取特定类型的链
        
        Args:
            text: 输入文本
            chain_type: 链类型
            context: 上下文信息
        
        Returns:
            链列表
        """
        extractor = self.extractors.get(chain_type)
        if not extractor:
            return []
        
        try:
            return extractor.extract(text, context)
        except Exception:
            return []
```

---

## 类图和时序图

### 类图

```
┌─────────────────────────────────────────────────────────────┐
│                   BaseExtractedChain                        │
│  ├─ chain_id: str                                           │
│  ├─ chain_type: ChainType                                   │
│  ├─ content: str                                            │
│  ├─ extraction_confidence: float                            │
│  ├─ to_summary(): str  {abstract}                           │
│  └─ to_dict(): dict                                         │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬────────────┐
        │            │            │            │
        ▼            ▼            ▼            ▼
┌───────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ExtractedCausal│ │Extracted │ │Extracted │ │Extracted │
│Chain          │ │LogicChain│ │Operation │ │Narrative │
│               │ │          │ │Chain     │ │Chain     │
│- problem      │ │- premises│ │- steps   │ │- events  │
│- causes       │ │- inference│ │- outcome │ │- arc     │
│- solutions    │ │- conclusion│          │          │
└───────────────┘ └──────────┘ └──────────┘ └──────────┘

┌─────────────────────────────────────────────────────────────┐
│                   BaseChainExtractor                        │
│  ├─ extract(text, context): List[Chain]  {abstract}        │
│  └─ get_chain_type(): ChainType  {abstract}                │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌───────────────┐ ┌──────────┐ ┌──────────┐
│CausalChain    │ │LogicChain│ │Operation │
│Extractor      │ │Extractor │ │Chain     │
│               │ │          │ │Extractor │
└───────────────┘ └──────────┘ └──────────┘

┌─────────────────────────────────────────────────────────────┐
│              ChainExtractorOrchestrator                      │
│  ├─ extractors: Dict[ChainType, Extractor]                 │
│  ├─ register_extractor(extractor)                          │
│  ├─ extract_all_chains(text): Dict                         │
│  └─ extract_specific_chain(text, type): List               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   ChainStorageManager                       │
│  ├─ short_term: ShortTermMemoryManager                     │
│  ├─ store_chain(chain, bucket): str                         │
│  └─ retrieve_chains(type, bucket, limit): List             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     ChainBuffer                             │
│  ├─ buffer_id: str                                         │
│  ├─ buffer_type: ChainType                                 │
│  ├─ chains: List[BaseExtractedChain]                       │
│  ├─ max_capacity: int                                      │
│  ├─ ttl_minutes: int                                       │
│  ├─ add_chain(chain): bool                                 │
│  └─ cleanup_expired(): int                                 │
└─────────────────────────────────────────────────────────────┘
```

### 时序图：提取与存储流程

```
用户输入文本
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│              ChainExtractorOrchestrator                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ├─→ CausalChainExtractor
                     │      │
                     │      ├─→ 提取问题
                     │      ├─→ 提取原因
                     │      ├─→ 提取解决方案
                     │      └─→ 返回 ExtractedCausalChain
                     │
                     ├─→ LogicChainExtractor
                     │      │
                     │      ├─→ 提取前提
                     │      ├─→ 提取推理步骤
                     │      └─→ 返回 ExtractedLogicChain
                     │
                     └─→ OperationChainExtractor
                            │
                            ├─→ 提取操作步骤
                            └─→ 返回 ExtractedOperationChain
                     │
                     ▼
              返回 Dict[ChainType, List[Chain]]
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   ChainStorageManager                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ├─→ 遍历所有链
                     │      │
                     │      ├─→ 推断桶类型
                     │      ├─→ 序列化链数据
                     │      └─→ 存储到短期记忆
                     │
                     ▼
              返回 List[item_id]
```

---

## 关键算法说明

### 1. 相似度计算算法

```python
from typing import Set
import math

def calculate_similarity(keywords1: Set[str], keywords2: Set[str]) -> float:
    """
    计算两个关键词集合的余弦相似度
    
    Args:
        keywords1: 关键词集合1
        keywords2: 关键词集合2
    
    Returns:
        相似度分数（0-1）
    """
    if not keywords1 or not keywords2:
        return 0.0
    
    # 计算交集
    intersection = keywords1 & keywords2
    
    # 计算余弦相似度
    similarity = len(intersection) / math.sqrt(
        len(keywords1) * len(keywords2)
    )
    
    return similarity
```

### 2. 聚类算法

```python
from typing import List
from collections import defaultdict

class TopicClusterer:
    """话题聚类器"""
    
    def __init__(self, similarity_threshold: float = 0.3):
        self.similarity_threshold = similarity_threshold
    
    def cluster_items(
        self,
        items: List[ShortTermMemoryItem]
    ) -> List[TopicCluster]:
        """
        聚类记忆项
        
        Args:
            items: 记忆项列表
        
        Returns:
            话题簇列表
        """
        if not items:
            return []
        
        # 提取所有项的关键词
        item_keywords = {
            item.item_id: extract_keywords(item.content)
            for item in items
        }
        
        # 初始化簇
        clusters: List[TopicCluster] = []
        assigned_items: Set[str] = set()
        
        # 对每个未分配的项
        for item in items:
            if item.item_id in assigned_items:
                continue
            
            # 创建新簇
            cluster = TopicCluster(
                cluster_id=f"cluster_{len(clusters)}",
                topic_label="",
                dominant_bucket=item.bucket_type
            )
            
            # 找到相似的项
            similar_items = self._find_similar_items(
                item,
                items,
                item_keywords,
                assigned_items
            )
            
            # 添加到簇
            for similar_item in similar_items:
                cluster.add_item(similar_item)
                assigned_items.add(similar_item.item_id)
            
            # 设置话题标签
            cluster.topic_label = self._generate_topic_label(
                cluster.keywords
            )
            
            clusters.append(cluster)
        
        return clusters
    
    def _find_similar_items(
        self,
        target_item: ShortTermMemoryItem,
        all_items: List[ShortTermMemoryItem],
        item_keywords: Dict[str, Set[str]],
        assigned_items: Set[str]
    ) -> List[ShortTermMemoryItem]:
        """找到相似的项"""
        similar_items = [target_item]
        target_keywords = item_keywords[target_item.item_id]
        
        for item in all_items:
            if item.item_id == target_item.item_id:
                continue
            
            if item.item_id in assigned_items:
                continue
            
            item_kw = item_keywords[item.item_id]
            similarity = calculate_similarity(target_keywords, item_kw)
            
            if similarity >= self.similarity_threshold:
                similar_items.append(item)
        
        return similar_items
    
    def _generate_topic_label(self, keywords: Set[str]) -> str:
        """生成话题标签"""
        if not keywords:
            return "未分类话题"
        
        # 取前3个关键词
        top_keywords = sorted(list(keywords))[:3]
        return "、".join(top_keywords)
```

### 3. 关联算法

```python
class BucketChainLinker:
    """桶-链关联器"""
    
    def link_buckets_and_chains(
        self,
        clusters: List[TopicCluster],
        chains: Dict[ChainType, List[BaseExtractedChain]]
    ) -> List[BucketChainLink]:
        """
        关联桶和链
        
        Args:
            clusters: 话题簇列表
            chains: 链映射
        
        Returns:
            关联列表
        """
        links = []
        
        for cluster in clusters:
            for chain_type, chain_list in chains.items():
                for chain in chain_list:
                    # 计算关联强度
                    strength = self._calculate_link_strength(
                        cluster, chain
                    )
                    
                    if strength > 0.5:
                        link = BucketChainLink(
                            cluster_id=cluster.cluster_id,
                            chain_id=chain.chain_id,
                            link_type=self._determine_link_type(
                                cluster, chain
                            ),
                            strength=strength,
                            evidence=self._collect_evidence(
                                cluster, chain
                            )
                        )
                        links.append(link)
                        
                        # 更新簇的关联信息
                        cluster.related_chains.append(chain.chain_id)
        
        return links
    
    def _calculate_link_strength(
        self,
        cluster: TopicCluster,
        chain: BaseExtractedChain
    ) -> float:
        """计算关联强度"""
        # 策略1：内容匹配
        content_match = self._content_matching_score(cluster, chain)
        
        # 策略2：关键词重叠
        keyword_overlap = self._keyword_overlap_score(cluster, chain)
        
        # 综合评分
        strength = (content_match + keyword_overlap) / 2.0
        
        return strength
    
    def _content_matching_score(
        self,
        cluster: TopicCluster,
        chain: BaseExtractedChain
    ) -> float:
        """内容匹配评分"""
        cluster_text = " ".join([item.content for item in cluster.items])
        chain_text = chain.content
        
        # 简单的词重叠计算
        cluster_words = set(cluster_text.split())
        chain_words = set(chain_text.split())
        
        overlap = cluster_words & chain_words
        if not chain_words:
            return 0.0
        
        return len(overlap) / len(chain_words)
    
    def _keyword_overlap_score(
        self,
        cluster: TopicCluster,
        chain: BaseExtractedChain
    ) -> float:
        """关键词重叠评分"""
        chain_keywords = extract_keywords(chain.content)
        overlap = cluster.keywords & chain_keywords
        
        if not chain_keywords:
            return 0.0
        
        return len(overlap) / len(chain_keywords)
```

### 4. 交叉验证算法

```python
class CrossValidator:
    """交叉验证器"""
    
    def validate_consistency(
        self,
        cluster: TopicCluster,
        chain: BaseExtractedChain
    ) -> ValidationResult:
        """
        验证一致性
        
        Args:
            cluster: 话题簇
            chain: 链
        
        Returns:
            验证结果
        """
        issues = []
        
        # 根据链类型选择验证策略
        if chain.chain_type == ChainType.CAUSAL:
            issues.extend(self._validate_causal_consistency(cluster, chain))
        elif chain.chain_type == ChainType.LOGIC:
            issues.extend(self._validate_logic_consistency(cluster, chain))
        elif chain.chain_type == ChainType.OPERATION:
            issues.extend(self._validate_operation_consistency(cluster, chain))
        elif chain.chain_type == ChainType.NARRATIVE:
            issues.extend(self._validate_narrative_consistency(cluster, chain))
        elif chain.chain_type == ChainType.TIME:
            issues.extend(self._validate_time_consistency(cluster, chain))
        
        # 计算置信度
        confidence = 1.0 - len(issues) * 0.2
        
        return ValidationResult(
            validation_type=f"{chain.chain_type}_consistency",
            passed=len(issues) == 0,
            confidence=max(0.0, confidence),
            issues=issues,
            suggestions=self._generate_suggestions(issues)
        )
    
    def _validate_causal_consistency(
        self,
        cluster: TopicCluster,
        chain: BaseExtractedChain
    ) -> List[str]:
        """验证因果一致性"""
        issues = []
        
        if not isinstance(chain, ExtractedCausalChain):
            return issues
        
        # 检查：问题是否在簇中
        problem_keywords = extract_keywords(chain.problem.content)
        if not problem_keywords & cluster.keywords:
            issues.append("因果链的问题与话题簇关键词不匹配")
        
        # 检查：原因是否合理
        for cause in chain.causes:
            cause_keywords = extract_keywords(cause.content)
            if not cause_keywords & cluster.keywords:
                issues.append(f"原因 '{cause.content}' 与话题簇不匹配")
        
        return issues
```

---

## 总结

本文档详细描述了双轨并行架构的数据结构、接口定义、类图和关键算法。核心设计包括：

1. **统一的数据模型**：BaseExtractedChain 基类 + 5种派生类
2. **清晰的接口定义**：提取器、存储管理器、编排器
3. **完整的算法实现**：相似度、聚类、关联、验证
4. **可扩展的架构**：插件化设计，易于添加新链类型

这些设计为后续的实施提供了坚实的基础。
