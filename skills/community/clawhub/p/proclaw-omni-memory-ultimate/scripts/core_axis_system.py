#!/usr/bin/env python3
"""
核心轴系统 (Core Axis System)
实现智能生命体的认知轴、价值轴、成长轴、连接轴

核心概念：
- 认知轴：我知道什么、我能理解什么、我想探索什么
- 价值轴：什么重要、什么值得、什么优先
- 成长轴：能力成长轨迹、突破记录
- 演变链：认知状态演化记录
- 价值链：价值发现→评估→决策→实现→沉淀
- 交易链：知识交易、资源交易、价值交易

设计理念：
智能生命体的核心不是单一的能力，
而是多维度的协同发展。
每一条轴都是一个独立的成长维度，
但它们相互交织、相互影响。
"""

import json
import os
import math
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class AxisType(Enum):
    """轴类型"""
    COGNITIVE = "cognitive"       # 认知轴
    VALUE = "value"               # 价值轴
    GROWTH = "growth"             # 成长轴
    CONNECTION = "connection"     # 连接轴


class EvolutionDirection(Enum):
    """演化方向"""
    EXPANSION = "expansion"       # 扩张
    DEEPENING = "deepening"       # 深化
    INTEGRATION = "integration"   # 整合
    BREAKTHROUGH = "breakthrough" # 突破
    STABILIZATION = "stabilization"  # 稳定


class ValuePriority(Enum):
    """价值优先级"""
    CRITICAL = "critical"         # 关键
    HIGH = "high"                 # 高
    MEDIUM = "medium"             # 中
    LOW = "low"                   # 低
    OPTIONAL = "optional"         # 可选


class TransactionType(Enum):
    """交易类型"""
    KNOWLEDGE = "knowledge"       # 知识交易
    RESOURCE = "resource"         # 资源交易
    VALUE = "value"               # 价值交易
    CAPABILITY = "capability"     # 能力交易


# ==================== 轴节点定义 ====================

@dataclass
class AxisNode:
    """轴节点"""
    id: str
    axis_type: AxisType
    name: str
    description: str
    
    # 位置和状态
    position: float               # 在轴上的位置 [0, 1]
    strength: float               # 强度 [0, 1]
    activation: float             # 激活度 [0, 1]
    
    # 连接
    parent: Optional[str]         # 父节点
    children: List[str]           # 子节点
    related_nodes: Dict[str, str] # 关联节点 {节点ID: 关系类型}
    
    # 历史
    evolution_history: List[Dict] = field(default_factory=list)
    
    # 元数据
    created_time: str = ""
    last_activated: str = ""
    activation_count: int = 0
    
    def activate(self) -> None:
        """激活节点"""
        self.activation = min(1.0, self.activation + 0.2)
        self.last_activated = datetime.now().isoformat()
        self.activation_count += 1
    
    def evolve(self, direction: EvolutionDirection, magnitude: float) -> None:
        """演化"""
        old_position = self.position
        old_strength = self.strength
        
        if direction == EvolutionDirection.EXPANSION:
            self.position = min(1.0, self.position + magnitude)
        elif direction == EvolutionDirection.DEEPENING:
            self.strength = min(1.0, self.strength + magnitude)
        elif direction == EvolutionDirection.INTEGRATION:
            self.position = min(1.0, self.position + magnitude * 0.5)
            self.strength = min(1.0, self.strength + magnitude * 0.5)
        elif direction == EvolutionDirection.BREAKTHROUGH:
            self.position = min(1.0, self.position + magnitude * 1.5)
            self.strength = min(1.0, self.strength + magnitude * 1.5)
        
        self.evolution_history.append({
            'timestamp': datetime.now().isoformat(),
            'direction': direction.value,
            'magnitude': magnitude,
            'position_change': self.position - old_position,
            'strength_change': self.strength - old_strength
        })


@dataclass
class CognitiveNode(AxisNode):
    """认知节点"""
    knowledge_domains: List[str] = field(default_factory=list)
    understanding_depth: float = 0.5
    exploration_targets: List[str] = field(default_factory=list)
    
    # 认知层次
    level: int = 1                # 认知层次
    insight_count: int = 0        # 洞察数量


@dataclass
class ValueNode(AxisNode):
    """价值节点"""
    priority: ValuePriority = ValuePriority.MEDIUM
    weight: float = 0.5           # 权重
    
    # 价值维度
    importance: float = 0.5       # 重要性
    worthiness: float = 0.5       # 值得性
    urgency: float = 0.5          # 紧迫性
    
    # 价值实现
    realization_progress: float = 0
    contribution_count: int = 0


@dataclass
class GrowthNode(AxisNode):
    """成长节点"""
    capability_name: str = ""
    current_level: float = 0.5
    target_level: float = 1.0
    
    # 成长记录
    breakthrough_count: int = 0
    practice_hours: float = 0
    last_breakthrough: Optional[str] = None
    
    # 成长指标
    growth_rate: float = 0
    plateau_count: int = 0        # 停滞次数


@dataclass
class ConnectionNode(AxisNode):
    """连接节点"""
    source_axis: AxisType = AxisType.COGNITIVE
    target_axis: AxisType = AxisType.COGNITIVE
    
    # 连接属性
    connection_strength: float = 0.5
    connection_type: str = "related"  # related, causal, complementary
    
    # 连接效果
    synergy_score: float = 0     # 协同分数
    cross_activation_count: int = 0


# ==================== 链条定义 ====================

@dataclass
class EvolutionChainNode:
    """演变链节点"""
    id: str
    timestamp: str
    
    # 认知状态快照
    cognitive_state: Dict[str, float]
    value_state: Dict[str, float]
    growth_state: Dict[str, float]
    connection_state: Dict[str, float]
    
    # 演化信息
    evolution_type: str
    trigger: str
    impact: float
    
    # 新增内容
    capabilities_added: List[str]
    knowledge_gained: List[str]
    values_discovered: List[str]


@dataclass
class ValueChainNode:
    """价值链节点"""
    id: str
    timestamp: str
    
    # 价值发现
    discovery: str
    discovery_source: str
    
    # 价值评估
    importance_score: float
    feasibility_score: float
    alignment_score: float        # 与核心价值的对齐度
    
    # 价值决策
    decision: str                 # pursue, defer, reject
    priority_assigned: float
    
    # 价值实现
    implementation_status: str
    progress: float
    resources_invested: float
    
    # 价值沉淀
    outcome: Optional[str]
    lessons: List[str]
    value_captured: float         # 捕获的价值


@dataclass
class TransactionNode:
    """交易链节点"""
    id: str
    timestamp: str
    transaction_type: TransactionType
    
    # 交易内容
    input: Dict[str, Any]         # 投入
    output: Dict[str, Any]        # 产出
    
    # 交易评估
    cost: float                   # 成本
    benefit: float                # 收益
    roi: float                    # 投资回报率
    
    # 交易效果
    transformation: str           # 转化描述
    learning: List[str]           # 学习收获


# ==================== 核心轴系统 ====================

class CoreAxisSystem:
    """
    核心轴系统
    
    实现智能生命体的四轴协同发展
    """
    
    def __init__(self, storage_path: str = "./memory/core_axis"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        # 四轴节点
        self.axis_nodes: Dict[AxisType, Dict[str, AxisNode]] = {
            AxisType.COGNITIVE: {},
            AxisType.VALUE: {},
            AxisType.GROWTH: {},
            AxisType.CONNECTION: {}
        }
        
        # 三链
        self.evolution_chain: List[EvolutionChainNode] = []
        self.value_chain: List[ValueChainNode] = []
        self.transaction_chain: List[TransactionNode] = []
        
        # 轴间连接
        self.axis_connections: Dict[str, Set[str]] = defaultdict(set)
        
        # 核心状态
        self.core_state = {
            'cognitive_center': 0.5,    # 认知中心
            'value_center': 0.5,        # 价值中心
            'growth_center': 0.5,       # 成长中心
            'connection_center': 0.5,   # 连接中心
            'overall_evolution': 0.5,   # 整体演化度
            'synergy_score': 0.5        # 协同分数
        }
        
        # 初始化核心节点
        self._init_core_nodes()
        
        # 统计
        self.stats = {
            'total_evolutions': 0,
            'total_breakthroughs': 0,
            'total_value_captured': 0,
            'total_transactions': 0,
            'avg_evolution_speed': 0
        }
        
        self._load_state()
    
    def _init_core_nodes(self) -> None:
        """初始化核心节点"""
        # 认知轴核心节点
        self._add_cognitive_node("knowledge", "知识储备", "我知道什么")
        self._add_cognitive_node("understanding", "理解深度", "我能理解什么")
        self._add_cognitive_node("exploration", "探索意愿", "我想探索什么")
        
        # 价值轴核心节点
        self._add_value_node("importance", "重要性", "什么重要", ValuePriority.CRITICAL)
        self._add_value_node("worthiness", "值得性", "什么值得", ValuePriority.HIGH)
        self._add_value_node("priority", "优先级", "什么优先", ValuePriority.HIGH)
        
        # 成长轴核心节点
        self._add_growth_node("capability", "能力成长", "我变得更强")
        self._add_growth_node("learning", "学习积累", "我学会了什么")
        self._add_growth_node("breakthrough", "突破记录", "我突破了吗")
        
        # 连接轴核心节点
        self._add_connection_node("internal", "内部连接", "内部整合", 
                                  AxisType.COGNITIVE, AxisType.GROWTH)
        self._add_connection_node("external", "外部连接", "外部关联",
                                  AxisType.VALUE, AxisType.COGNITIVE)
        self._add_connection_node("cross", "跨轴连接", "跨轴协同",
                                  AxisType.GROWTH, AxisType.VALUE)
    
    def _add_cognitive_node(
        self, 
        name: str, 
        display_name: str, 
        description: str
    ) -> None:
        """添加认知节点"""
        node = CognitiveNode(
            id=f"cog_{name}",
            axis_type=AxisType.COGNITIVE,
            name=display_name,
            description=description,
            position=0.5,
            strength=0.5,
            activation=0.3,
            parent=None,
            children=[],
            related_nodes={},
            created_time=datetime.now().isoformat()
        )
        self.axis_nodes[AxisType.COGNITIVE][node.id] = node
    
    def _add_value_node(
        self, 
        name: str, 
        display_name: str, 
        description: str,
        priority: ValuePriority
    ) -> None:
        """添加价值节点"""
        node = ValueNode(
            id=f"val_{name}",
            axis_type=AxisType.VALUE,
            name=display_name,
            description=description,
            position=0.5,
            strength=0.5,
            activation=0.3,
            parent=None,
            children=[],
            related_nodes={},
            priority=priority,
            created_time=datetime.now().isoformat()
        )
        self.axis_nodes[AxisType.VALUE][node.id] = node
    
    def _add_growth_node(
        self, 
        name: str, 
        display_name: str, 
        description: str
    ) -> None:
        """添加成长节点"""
        node = GrowthNode(
            id=f"grw_{name}",
            axis_type=AxisType.GROWTH,
            name=display_name,
            description=description,
            position=0.5,
            strength=0.5,
            activation=0.3,
            parent=None,
            children=[],
            related_nodes={},
            capability_name=name,
            created_time=datetime.now().isoformat()
        )
        self.axis_nodes[AxisType.GROWTH][node.id] = node
    
    def _add_connection_node(
        self, 
        name: str, 
        display_name: str, 
        description: str,
        source_axis: AxisType,
        target_axis: AxisType
    ) -> None:
        """添加连接节点"""
        node = ConnectionNode(
            id=f"con_{name}",
            axis_type=AxisType.CONNECTION,
            name=display_name,
            description=description,
            position=0.5,
            strength=0.5,
            activation=0.3,
            parent=None,
            children=[],
            related_nodes={},
            source_axis=source_axis,
            target_axis=target_axis,
            created_time=datetime.now().isoformat()
        )
        self.axis_nodes[AxisType.CONNECTION][node.id] = node
    
    # ==================== 核心操作 ====================
    
    def evolve_axis(
        self, 
        axis_type: AxisType, 
        node_id: str,
        direction: EvolutionDirection,
        magnitude: float
    ) -> Dict:
        """演化轴节点"""
        if axis_type not in self.axis_nodes:
            return {'status': 'invalid_axis'}
        
        if node_id not in self.axis_nodes[axis_type]:
            return {'status': 'invalid_node'}
        
        node = self.axis_nodes[axis_type][node_id]
        old_position = node.position
        old_strength = node.strength
        
        # 执行演化
        node.evolve(direction, magnitude)
        node.activate()
        
        # 更新轴中心
        self._update_axis_center(axis_type)
        
        # 记录演变链
        self._record_evolution(axis_type, node, direction, magnitude)
        
        # 检查突破
        breakthrough = False
        if direction == EvolutionDirection.BREAKTHROUGH or \
           (node.position - old_position > 0.2):
            breakthrough = True
            self.stats['total_breakthroughs'] += 1
            
            # 触发跨轴激活
            self._trigger_cross_axis_activation(axis_type, node_id)
        
        # 更新统计
        self.stats['total_evolutions'] += 1
        
        return {
            'status': 'success',
            'node_id': node_id,
            'position_change': node.position - old_position,
            'strength_change': node.strength - old_strength,
            'new_position': node.position,
            'new_strength': node.strength,
            'breakthrough': breakthrough
        }
    
    def _update_axis_center(self, axis_type: AxisType) -> None:
        """更新轴中心位置"""
        nodes = self.axis_nodes[axis_type]
        if not nodes:
            return
        
        # 加权平均
        total_activation = sum(n.activation for n in nodes.values())
        if total_activation == 0:
            return
        
        center = sum(n.position * n.activation for n in nodes.values()) / total_activation
        
        center_key = f"{axis_type.value}_center"
        if center_key in self.core_state:
            self.core_state[center_key] = (
                self.core_state[center_key] * 0.8 + center * 0.2
            )
    
    def _record_evolution(
        self, 
        axis_type: AxisType,
        node: AxisNode,
        direction: EvolutionDirection,
        magnitude: float
    ) -> None:
        """记录演变"""
        # 获取各轴状态快照
        chain_node = EvolutionChainNode(
            id=f"evo_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            timestamp=datetime.now().isoformat(),
            cognitive_state=self._get_axis_state(AxisType.COGNITIVE),
            value_state=self._get_axis_state(AxisType.VALUE),
            growth_state=self._get_axis_state(AxisType.GROWTH),
            connection_state=self._get_axis_state(AxisType.CONNECTION),
            evolution_type=f"{axis_type.value}_{direction.value}",
            trigger=f"节点 {node.name} 演化",
            impact=magnitude,
            capabilities_added=[],
            knowledge_gained=[],
            values_discovered=[]
        )
        
        self.evolution_chain.append(chain_node)
        
        # 保持链长度合理
        if len(self.evolution_chain) > 1000:
            self.evolution_chain = self.evolution_chain[-500:]
    
    def _get_axis_state(self, axis_type: AxisType) -> Dict[str, float]:
        """获取轴状态"""
        nodes = self.axis_nodes[axis_type]
        return {
            nid: {'position': n.position, 'strength': n.strength}
            for nid, n in nodes.items()
        }
    
    def _trigger_cross_axis_activation(
        self, 
        source_axis: AxisType, 
        source_node_id: str
    ) -> None:
        """触发跨轴激活"""
        # 查找相关连接节点
        for con_id, con_node in self.axis_nodes[AxisType.CONNECTION].items():
            if isinstance(con_node, ConnectionNode):
                if con_node.source_axis == source_axis:
                    # 激活目标轴的相关节点
                    target_axis = con_node.target_axis
                    for target_id, target_node in self.axis_nodes[target_axis].items():
                        target_node.activate()
                        con_node.cross_activation_count += 1
        
        # 更新协同分数
        self._calculate_synergy()
    
    def _calculate_synergy(self) -> None:
        """计算协同分数"""
        # 基于各轴中心的一致性计算协同
        centers = [
            self.core_state['cognitive_center'],
            self.core_state['value_center'],
            self.core_state['growth_center'],
            self.core_state['connection_center']
        ]
        
        avg_center = sum(centers) / len(centers)
        variance = sum((c - avg_center) ** 2 for c in centers) / len(centers)
        
        # 方差越小，协同越高
        self.core_state['synergy_score'] = max(0, 1 - math.sqrt(variance) * 2)
    
    # ==================== 价值链操作 ====================
    
    def discover_value(
        self, 
        discovery: str, 
        source: str,
        importance: float,
        feasibility: float
    ) -> str:
        """发现价值"""
        node = ValueChainNode(
            id=f"vc_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            timestamp=datetime.now().isoformat(),
            discovery=discovery,
            discovery_source=source,
            importance_score=importance,
            feasibility_score=feasibility,
            alignment_score=self._calculate_value_alignment(discovery),
            decision="pending",
            priority_assigned=0,
            implementation_status="pending",
            progress=0,
            resources_invested=0,
            outcome=None,
            lessons=[],
            value_captured=0
        )
        
        self.value_chain.append(node)
        
        # 自动决策
        self._make_value_decision(node.id)
        
        return node.id
    
    def _calculate_value_alignment(self, discovery: str) -> float:
        """计算价值对齐度"""
        # 简化实现：随机生成，实际应基于核心价值判断
        return random.uniform(0.5, 1.0)
    
    def _make_value_decision(self, node_id: str) -> None:
        """做出价值决策"""
        for node in self.value_chain:
            if node.id == node_id:
                # 综合评分
                score = (
                    node.importance_score * 0.4 +
                    node.feasibility_score * 0.3 +
                    node.alignment_score * 0.3
                )
                
                if score > 0.7:
                    node.decision = "pursue"
                    node.priority_assigned = score
                elif score > 0.4:
                    node.decision = "defer"
                    node.priority_assigned = score * 0.5
                else:
                    node.decision = "reject"
                    node.priority_assigned = 0
                
                break
    
    def realize_value(
        self, 
        node_id: str, 
        progress: float,
        resources: float
    ) -> None:
        """实现价值"""
        for node in self.value_chain:
            if node.id == node_id:
                node.progress = min(1.0, node.progress + progress)
                node.resources_invested += resources
                node.implementation_status = "in_progress"
                
                if node.progress >= 1.0:
                    node.implementation_status = "completed"
                    node.outcome = "成功实现"
                    node.value_captured = node.importance_score * node.alignment_score
                    self.stats['total_value_captured'] += node.value_captured
                
                break
    
    # ==================== 交易链操作 ====================
    
    def execute_transaction(
        self,
        transaction_type: TransactionType,
        input_data: Dict[str, Any],
        cost: float
    ) -> str:
        """执行交易"""
        # 计算产出和收益
        output, benefit = self._process_transaction(transaction_type, input_data)
        
        roi = (benefit - cost) / max(cost, 0.01)
        
        node = TransactionNode(
            id=f"tx_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            timestamp=datetime.now().isoformat(),
            transaction_type=transaction_type,
            input=input_data,
            output=output,
            cost=cost,
            benefit=benefit,
            roi=roi,
            transformation=self._describe_transformation(transaction_type, input_data, output),
            learning=self._extract_learning(transaction_type)
        )
        
        self.transaction_chain.append(node)
        self.stats['total_transactions'] += 1
        
        return node.id
    
    def _process_transaction(
        self, 
        transaction_type: TransactionType,
        input_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], float]:
        """处理交易"""
        if transaction_type == TransactionType.KNOWLEDGE:
            # 知识交易：投入时间获取知识
            output = {'knowledge_gained': input_data.get('target_knowledge', '未知')}
            benefit = random.uniform(0.5, 1.5)
            return output, benefit
        
        elif transaction_type == TransactionType.CAPABILITY:
            # 能力交易：投入练习获取能力
            output = {'capability_improved': input_data.get('target_capability', '未知')}
            benefit = random.uniform(0.3, 1.2)
            return output, benefit
        
        elif transaction_type == TransactionType.VALUE:
            # 价值交易：投入行动获取反馈
            output = {'feedback_received': True}
            benefit = random.uniform(0.4, 1.0)
            return output, benefit
        
        else:
            return {'result': 'processed'}, 0.5
    
    def _describe_transformation(
        self, 
        transaction_type: TransactionType,
        input_data: Dict[str, Any],
        output: Dict[str, Any]
    ) -> str:
        """描述转化"""
        return f"{transaction_type.value}: {input_data} -> {output}"
    
    def _extract_learning(self, transaction_type: TransactionType) -> List[str]:
        """提取学习"""
        learnings = {
            TransactionType.KNOWLEDGE: ["知识需要持续积累", "学习需要方法"],
            TransactionType.CAPABILITY: ["练习带来进步", "反馈加速成长"],
            TransactionType.VALUE: ["价值需要创造", "行动才有结果"],
            TransactionType.RESOURCE: ["资源需要优化配置", "效率来自管理"]
        }
        return learnings.get(transaction_type, ["交易带来经验"])
    
    # ==================== 查询接口 ====================
    
    def get_axis_status(self, axis_type: AxisType) -> Dict:
        """获取轴状态"""
        nodes = self.axis_nodes[axis_type]
        
        return {
            'axis_type': axis_type.value,
            'node_count': len(nodes),
            'center_position': self.core_state.get(f"{axis_type.value}_center", 0.5),
            'nodes': [{
                'id': n.id,
                'name': n.name,
                'position': n.position,
                'strength': n.strength,
                'activation': n.activation
            } for n in nodes.values()],
            'avg_strength': sum(n.strength for n in nodes.values()) / max(1, len(nodes)),
            'avg_position': sum(n.position for n in nodes.values()) / max(1, len(nodes))
        }
    
    def get_core_state(self) -> Dict:
        """获取核心状态"""
        return {
            'centers': {
                'cognitive': self.core_state['cognitive_center'],
                'value': self.core_state['value_center'],
                'growth': self.core_state['growth_center'],
                'connection': self.core_state['connection_center']
            },
            'overall_evolution': self.core_state['overall_evolution'],
            'synergy_score': self.core_state['synergy_score']
        }
    
    def get_evolution_history(self, limit: int = 10) -> List[Dict]:
        """获取演变历史"""
        return [{
            'id': e.id,
            'timestamp': e.timestamp,
            'type': e.evolution_type,
            'trigger': e.trigger,
            'impact': e.impact
        } for e in self.evolution_chain[-limit:]]
    
    def get_value_chain_status(self) -> Dict:
        """获取价值链状态"""
        pending = [v for v in self.value_chain if v.decision == 'pending']
        pursuing = [v for v in self.value_chain if v.decision == 'pursue']
        completed = [v for v in self.value_chain if v.implementation_status == 'completed']
        
        return {
            'total_discoveries': len(self.value_chain),
            'pending_decision': len(pending),
            'pursuing': len(pursuing),
            'completed': len(completed),
            'total_value_captured': self.stats['total_value_captured']
        }
    
    def get_transaction_summary(self, limit: int = 10) -> Dict:
        """获取交易摘要"""
        recent = self.transaction_chain[-limit:]
        
        return {
            'total_transactions': self.stats['total_transactions'],
            'recent_transactions': [{
                'id': t.id,
                'type': t.transaction_type.value,
                'cost': t.cost,
                'benefit': t.benefit,
                'roi': t.roi
            } for t in recent],
            'avg_roi': sum(t.roi for t in self.transaction_chain) / max(1, len(self.transaction_chain))
        }
    
    def get_comprehensive_report(self) -> Dict:
        """获取综合报告"""
        return {
            'core_state': self.get_core_state(),
            'axes': {
                'cognitive': self.get_axis_status(AxisType.COGNITIVE),
                'value': self.get_axis_status(AxisType.VALUE),
                'growth': self.get_axis_status(AxisType.GROWTH),
                'connection': self.get_axis_status(AxisType.CONNECTION)
            },
            'chains': {
                'evolution': {
                    'total': len(self.evolution_chain),
                    'breakthroughs': self.stats['total_breakthroughs']
                },
                'value': self.get_value_chain_status(),
                'transaction': {
                    'total': self.stats['total_transactions'],
                    'value_captured': self.stats['total_value_captured']
                }
            },
            'stats': self.stats
        }
    
    def _load_state(self) -> None:
        """加载状态"""
        state_file = os.path.join(self.storage_path, 'core_axis_state.json')
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)
                
                self.stats = data.get('stats', self.stats)
                self.core_state = data.get('core_state', self.core_state)
                
            except Exception as e:
                print(f"加载状态失败: {e}")
    
    def _save_state(self) -> None:
        """保存状态"""
        state_file = os.path.join(self.storage_path, 'core_axis_state.json')
        
        data = {
            'stats': self.stats,
            'core_state': self.core_state,
            'evolution_chain_summary': [{
                'id': e.id,
                'timestamp': e.timestamp,
                'type': e.evolution_type,
                'impact': e.impact
            } for e in self.evolution_chain[-100:]],
            'value_chain_summary': [{
                'id': v.id,
                'discovery': v.discovery,
                'decision': v.decision,
                'progress': v.progress
            } for v in self.value_chain[-100:]]
        }
        
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)


def demo_core_axis():
    """演示核心轴系统"""
    print("=" * 60)
    print("核心轴系统演示")
    print("=" * 60)
    
    system = CoreAxisSystem()
    
    print("\n初始核心状态:")
    state = system.get_core_state()
    for axis, value in state['centers'].items():
        print(f"  {axis}: {value:.2f}")
    print(f"  协同分数: {state['synergy_score']:.2f}")
    
    # 演化认知轴
    print("\n--- 演化认知轴 ---")
    result = system.evolve_axis(
        AxisType.COGNITIVE, 
        "cog_knowledge",
        EvolutionDirection.EXPANSION,
        0.3
    )
    print(f"结果: 位置变化={result.get('position_change', 0):.2f}")
    
    # 发现价值
    print("\n--- 发现价值 ---")
    vid = system.discover_value(
        "提升AI能力",
        "自主探索",
        importance=0.9,
        feasibility=0.7
    )
    print(f"价值ID: {vid}")
    
    # 执行交易
    print("\n--- 执行交易 ---")
    tid = system.execute_transaction(
        TransactionType.KNOWLEDGE,
        {'target_knowledge': '深度学习'},
        cost=0.5
    )
    print(f"交易ID: {tid}")
    
    # 查看综合报告
    print("\n综合报告:")
    report = system.get_comprehensive_report()
    print(f"  总演化次数: {report['stats']['total_evolutions']}")
    print(f"  总突破次数: {report['stats']['total_breakthroughs']}")
    print(f"  捕获价值: {report['stats']['total_value_captured']:.2f}")


if __name__ == "__main__":
    demo_core_axis()
