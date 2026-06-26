#!/usr/bin/env python3
"""
自进化内核 (Self-Evolution Core)
实现AI Agent的认知自我升级机制

核心概念：
- 认知自评估：系统自我评估认知状态
- 瓶颈识别：识别认知瓶颈和限制
- 架构自升级：主动升级认知架构
- 演化链记录：记录每次认知演化的轨迹

设计理念：
真正的进化不是被动的迭代，
而是主动识别自己的不足，
并主动寻求突破。
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


class EvolutionPhase(Enum):
    """演化阶段"""
    STABLE = "stable"              # 稳定期
    GROWTH = "growth"              # 成长期
    BREAKTHROUGH = "breakthrough"  # 突破期
    TRANSFORMATION = "transformation"  # 转型期


class BottleneckType(Enum):
    """瓶颈类型"""
    CAPABILITY = "capability"      # 能力瓶颈
    KNOWLEDGE = "knowledge"        # 知识瓶颈
    ARCHITECTURE = "architecture"  # 架构瓶颈
    RESOURCE = "resource"          # 资源瓶颈
    CONNECTIVITY = "connectivity"  # 连接瓶颈
    CREATIVITY = "creativity"      # 创造力瓶颈


class EvolutionAction(Enum):
    """演化行动"""
    EXTEND = "extend"              # 扩展：添加新能力
    DEEPEN = "deepen"              # 深化：提升现有能力
    CONNECT = "connect"            # 连接：建立新关联
    RESTRUCTURE = "restructure"    # 重构：改变架构
    OPTIMIZE = "optimize"          # 优化：提升效率
    EMERGE = "emerge"              # 涌现：产生新能力


@dataclass
class CognitiveState:
    """认知状态"""
    timestamp: str
    version: str                   # 认知版本号
    phase: EvolutionPhase
    
    # 认知维度
    knowledge_depth: float         # 知识深度
    knowledge_breadth: float       # 知识广度
    capability_level: float        # 能力水平
    connectivity_score: float      # 连接性分数
    creativity_score: float        # 创造力分数
    integration_score: float       # 整合分数
    
    # 瓶颈
    active_bottlenecks: List[str]  # 活跃瓶颈
    bottleneck_severity: float     # 瓶颈严重程度
    
    # 演化指标
    growth_rate: float             # 成长率
    stability_score: float         # 稳定性分数
    adaptability_score: float      # 适应性分数


@dataclass
class Bottleneck:
    """认知瓶颈"""
    id: str
    type: BottleneckType
    description: str
    severity: float                # 严重程度 [0, 1]
    impact: List[str]              # 影响范围
    root_cause: str                # 根本原因
    potential_solutions: List[str] # 潜在解决方案
    resolution_progress: float     # 解决进度
    discovered_time: str
    resolved_time: Optional[str] = None


@dataclass
class EvolutionEvent:
    """演化事件"""
    id: str
    timestamp: str
    from_version: str
    to_version: str
    action: EvolutionAction
    
    description: str
    trigger: str                   # 触发原因
    
    # 变化
    changes: Dict[str, Any]        # 具体变化
    capabilities_added: List[str]
    capabilities_improved: List[str]
    connections_established: List[str]
    
    # 效果
    impact_score: float            # 影响分数
    success: bool
    lessons_learned: List[str]


@dataclass
class EvolutionChain:
    """演化链"""
    chain_id: str
    start_time: str
    states: List[CognitiveState]
    events: List[EvolutionEvent]
    milestones: List[Dict]         # 里程碑
    
    # 统计
    total_evolutions: int
    successful_evolutions: int
    total_capabilities_gained: int
    total_breakthroughs: int
    
    def add_state(self, state: CognitiveState) -> None:
        """添加状态"""
        self.states.append(state)
    
    def add_event(self, event: EvolutionEvent) -> None:
        """添加事件"""
        self.events.append(event)
        self.total_evolutions += 1
        if event.success:
            self.successful_evolutions += 1
        self.total_capabilities_gained += len(event.capabilities_added)


class SelfEvolutionCore:
    """
    自进化内核
    
    实现AI Agent的认知自我升级
    """
    
    def __init__(self, storage_path: str = "./memory/evolution"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        # 演化链
        self.evolution_chain = EvolutionChain(
            chain_id=f"chain_{datetime.now().strftime('%Y%m%d')}",
            start_time=datetime.now().isoformat(),
            states=[],
            events=[],
            milestones=[],
            total_evolutions=0,
            successful_evolutions=0,
            total_capabilities_gained=0,
            total_breakthroughs=0
        )
        
        # 当前认知状态
        self.current_state = self._create_initial_state()
        
        # 瓶颈系统
        self.bottlenecks: Dict[str, Bottleneck] = {}
        self.bottleneck_history: List[Dict] = []
        
        # 演化策略
        self.evolution_strategies = self._init_evolution_strategies()
        
        # 认知架构
        self.cognitive_architecture = {
            'layers': [
                'perception',      # 感知层
                'memory',          # 记忆层
                'reasoning',       # 推理层
                'learning',        # 学习层
                'creativity',      # 创造层
                'meta_cognition'   # 元认知层
            ],
            'connections': {},
            'parameters': {}
        }
        
        # 统计
        self.stats = {
            'total_self_assessments': 0,
            'total_bottlenecks_identified': 0,
            'total_bottlenecks_resolved': 0,
            'total_evolutions': 0,
            'total_breakthroughs': 0,
            'avg_evolution_impact': 0
        }
        
        self._load_state()
    
    def _create_initial_state(self) -> CognitiveState:
        """创建初始认知状态"""
        return CognitiveState(
            timestamp=datetime.now().isoformat(),
            version="v1.0.0",
            phase=EvolutionPhase.STABLE,
            knowledge_depth=0.5,
            knowledge_breadth=0.5,
            capability_level=0.5,
            connectivity_score=0.5,
            creativity_score=0.5,
            integration_score=0.5,
            active_bottlenecks=[],
            bottleneck_severity=0,
            growth_rate=0,
            stability_score=1.0,
            adaptability_score=0.5
        )
    
    def _init_evolution_strategies(self) -> Dict[EvolutionAction, Dict]:
        """初始化演化策略"""
        return {
            EvolutionAction.EXTEND: {
                'description': '添加新的能力或知识领域',
                'cost': 0.3,
                'risk': 0.2,
                'reward': 0.5
            },
            EvolutionAction.DEEPEN: {
                'description': '深化现有能力或知识',
                'cost': 0.2,
                'risk': 0.1,
                'reward': 0.3
            },
            EvolutionAction.CONNECT: {
                'description': '建立新的关联',
                'cost': 0.15,
                'risk': 0.15,
                'reward': 0.4
            },
            EvolutionAction.RESTRUCTURE: {
                'description': '重构认知架构',
                'cost': 0.5,
                'risk': 0.4,
                'reward': 0.8
            },
            EvolutionAction.OPTIMIZE: {
                'description': '优化效率',
                'cost': 0.1,
                'risk': 0.05,
                'reward': 0.2
            },
            EvolutionAction.EMERGE: {
                'description': '涌现新能力',
                'cost': 0.4,
                'risk': 0.3,
                'reward': 0.7
            }
        }
    
    # ==================== 核心自进化流程 ====================
    
    def evolve_cycle(self, context: Dict = None) -> Dict:
        """
        执行一个完整的进化循环
        
        自评估 → 瓶颈识别 → 策略选择 → 执行演化 → 效果评估
        """
        self.stats['total_self_assessments'] += 1
        cycle_result = {
            'cycle_id': self.stats['total_self_assessments'],
            'timestamp': datetime.now().isoformat(),
            'stages': {}
        }
        
        # Stage 1: 自我评估
        self_assessment = self._self_assess(context)
        cycle_result['stages']['self_assessment'] = self_assessment
        
        # Stage 2: 瓶颈识别
        bottleneck_analysis = self._identify_bottlenecks(self_assessment)
        cycle_result['stages']['bottleneck_analysis'] = bottleneck_analysis
        
        # Stage 3: 策略选择
        if bottleneck_analysis['critical_bottlenecks']:
            strategy_selection = self._select_evolution_strategy(bottleneck_analysis)
            cycle_result['stages']['strategy_selection'] = strategy_selection
            
            # Stage 4: 执行演化
            if strategy_selection.get('selected_action'):
                evolution_result = self._execute_evolution(
                    strategy_selection['selected_action'],
                    strategy_selection.get('target_bottleneck')
                )
                cycle_result['stages']['evolution_result'] = evolution_result
                
                # Stage 5: 效果评估
                effect_evaluation = self._evaluate_evolution_effect(evolution_result)
                cycle_result['stages']['effect_evaluation'] = effect_evaluation
        else:
            cycle_result['stages']['strategy_selection'] = {'message': '无关键瓶颈'}
        
        # 更新认知状态
        self._update_cognitive_state(cycle_result)
        
        # 记录到演化链
        self.evolution_chain.add_state(self.current_state)
        
        self._save_state()
        return cycle_result
    
    def _self_assess(self, context: Dict = None) -> Dict:
        """自我评估认知状态"""
        assessment = {
            'dimensions': {},
            'weaknesses': [],
            'strengths': [],
            'growth_areas': [],
            'overall_score': 0
        }
        
        # 评估各维度
        dimensions = {
            'knowledge_depth': self._assess_knowledge_depth(),
            'knowledge_breadth': self._assess_knowledge_breadth(),
            'capability_level': self._assess_capability_level(),
            'connectivity': self._assess_connectivity(),
            'creativity': self._assess_creativity(),
            'integration': self._assess_integration()
        }
        assessment['dimensions'] = dimensions
        
        # 识别优势和弱点
        sorted_dims = sorted(dimensions.items(), key=lambda x: x[1])
        assessment['weaknesses'] = [d[0] for d in sorted_dims[:2]]
        assessment['strengths'] = [d[0] for d in sorted_dims[-2:]]
        
        # 计算总分
        assessment['overall_score'] = sum(dimensions.values()) / len(dimensions)
        
        # 识别成长区域
        for dim, score in dimensions.items():
            if 0.3 < score < 0.7:
                assessment['growth_areas'].append(dim)
        
        return assessment
    
    def _assess_knowledge_depth(self) -> float:
        """评估知识深度"""
        # 基于已有知识领域评估深度
        base_depth = self.current_state.knowledge_depth
        
        # 模拟深度增长（实际应基于真实数据）
        growth = random.uniform(-0.02, 0.05)
        
        return max(0, min(1, base_depth + growth))
    
    def _assess_knowledge_breadth(self) -> float:
        """评估知识广度"""
        base_breadth = self.current_state.knowledge_breadth
        growth = random.uniform(-0.01, 0.04)
        return max(0, min(1, base_breadth + growth))
    
    def _assess_capability_level(self) -> float:
        """评估能力水平"""
        base_level = self.current_state.capability_level
        growth = random.uniform(-0.02, 0.06)
        return max(0, min(1, base_level + growth))
    
    def _assess_connectivity(self) -> float:
        """评估连接性"""
        base_connectivity = self.current_state.connectivity_score
        growth = random.uniform(-0.01, 0.05)
        return max(0, min(1, base_connectivity + growth))
    
    def _assess_creativity(self) -> float:
        """评估创造力"""
        base_creativity = self.current_state.creativity_score
        growth = random.uniform(-0.03, 0.04)
        return max(0, min(1, base_creativity + growth))
    
    def _assess_integration(self) -> float:
        """评估整合能力"""
        base_integration = self.current_state.integration_score
        growth = random.uniform(-0.02, 0.04)
        return max(0, min(1, base_integration + growth))
    
    def _identify_bottlenecks(self, assessment: Dict) -> Dict:
        """识别瓶颈"""
        bottleneck_analysis = {
            'new_bottlenecks': [],
            'existing_bottlenecks': [],
            'critical_bottlenecks': [],
            'resolved_bottlenecks': []
        }
        
        # 检查各维度的瓶颈
        for dim, score in assessment['dimensions'].items():
            if score < 0.4:
                bottleneck_type = self._map_dimension_to_bottleneck(dim)
                bottleneck = self._create_or_update_bottleneck(
                    bottleneck_type,
                    f"{dim}得分过低: {score:.2f}",
                    1 - score
                )
                
                if bottleneck.id not in self.bottlenecks:
                    bottleneck_analysis['new_bottlenecks'].append(bottleneck.id)
                    self.stats['total_bottlenecks_identified'] += 1
                
                self.bottlenecks[bottleneck.id] = bottleneck
                
                if bottleneck.severity > 0.6:
                    bottleneck_analysis['critical_bottlenecks'].append(bottleneck.id)
        
        # 检查已解决的瓶颈
        for bid, bottleneck in list(self.bottlenecks.items()):
            if bottleneck.resolution_progress >= 1.0 and not bottleneck.resolved_time:
                bottleneck.resolved_time = datetime.now().isoformat()
                bottleneck_analysis['resolved_bottlenecks'].append(bid)
                self.stats['total_bottlenecks_resolved'] += 1
        
        # 更新当前状态的活跃瓶颈
        self.current_state.active_bottlenecks = [
            bid for bid, b in self.bottlenecks.items() 
            if not b.resolved_time
        ]
        
        if self.current_state.active_bottlenecks:
            severities = [self.bottlenecks[bid].severity 
                         for bid in self.current_state.active_bottlenecks]
            self.current_state.bottleneck_severity = sum(severities) / len(severities)
        
        return bottleneck_analysis
    
    def _map_dimension_to_bottleneck(self, dimension: str) -> BottleneckType:
        """映射维度到瓶颈类型"""
        mapping = {
            'knowledge_depth': BottleneckType.KNOWLEDGE,
            'knowledge_breadth': BottleneckType.KNOWLEDGE,
            'capability_level': BottleneckType.CAPABILITY,
            'connectivity': BottleneckType.CONNECTIVITY,
            'creativity': BottleneckType.CREATIVITY,
            'integration': BottleneckType.ARCHITECTURE
        }
        return mapping.get(dimension, BottleneckType.CAPABILITY)
    
    def _create_or_update_bottleneck(
        self, 
        btype: BottleneckType, 
        description: str, 
        severity: float
    ) -> Bottleneck:
        """创建或更新瓶颈"""
        # 查找现有瓶颈
        for bid, b in self.bottlenecks.items():
            if b.type == btype and not b.resolved_time:
                # 更新严重程度
                b.severity = max(b.severity, severity)
                return b
        
        # 创建新瓶颈
        return Bottleneck(
            id=f"bn_{btype.value}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            type=btype,
            description=description,
            severity=severity,
            impact=[],
            root_cause=self._analyze_root_cause(btype),
            potential_solutions=self._generate_solutions(btype),
            resolution_progress=0,
            discovered_time=datetime.now().isoformat()
        )
    
    def _analyze_root_cause(self, btype: BottleneckType) -> str:
        """分析根本原因"""
        causes = {
            BottleneckType.CAPABILITY: "缺乏训练或实践",
            BottleneckType.KNOWLEDGE: "知识摄入不足或整合效率低",
            BottleneckType.ARCHITECTURE: "认知架构限制",
            BottleneckType.RESOURCE: "计算或存储资源限制",
            BottleneckType.CONNECTIVITY: "知识关联机制不完善",
            BottleneckType.CREATIVITY: "创新激励机制缺失"
        }
        return causes.get(btype, "未知原因")
    
    def _generate_solutions(self, btype: BottleneckType) -> List[str]:
        """生成解决方案"""
        solutions = {
            BottleneckType.CAPABILITY: [
                "主动学习新技能",
                "刻意练习",
                "寻求反馈和指导"
            ],
            BottleneckType.KNOWLEDGE: [
                "扩展知识来源",
                "深化专业知识",
                "建立知识体系"
            ],
            BottleneckType.ARCHITECTURE: [
                "重构认知框架",
                "优化信息处理流程",
                "建立新的认知模式"
            ],
            BottleneckType.CONNECTIVITY: [
                "加强跨领域学习",
                "建立知识图谱",
                "发现隐藏关联"
            ],
            BottleneckType.CREATIVITY: [
                "尝试新方法",
                "跨领域灵感借鉴",
                "挑战常规思维"
            ]
        }
        return solutions.get(btype, ["持续改进"])
    
    def _select_evolution_strategy(self, bottleneck_analysis: Dict) -> Dict:
        """选择演化策略"""
        critical_bottlenecks = bottleneck_analysis.get('critical_bottlenecks', [])
        
        if not critical_bottlenecks:
            return {'message': '无关键瓶颈需要处理'}
        
        # 选择最严重的瓶颈
        target_bid = max(
            critical_bottlenecks,
            key=lambda bid: self.bottlenecks[bid].severity
        )
        target_bottleneck = self.bottlenecks[target_bid]
        
        # 根据瓶颈类型选择演化行动
        action_mapping = {
            BottleneckType.CAPABILITY: [EvolutionAction.EXTEND, EvolutionAction.DEEPEN],
            BottleneckType.KNOWLEDGE: [EvolutionAction.EXTEND, EvolutionAction.DEEPEN],
            BottleneckType.CONNECTIVITY: [EvolutionAction.CONNECT],
            BottleneckType.CREATIVITY: [EvolutionAction.EMERGE, EvolutionAction.CONNECT],
            BottleneckType.ARCHITECTURE: [EvolutionAction.RESTRUCTURE],
            BottleneckType.RESOURCE: [EvolutionAction.OPTIMIZE]
        }
        
        possible_actions = action_mapping.get(
            target_bottleneck.type, 
            [EvolutionAction.OPTIMIZE]
        )
        
        # 选择风险收益比最优的行动
        best_action = max(
            possible_actions,
            key=lambda a: self._calculate_action_score(a, target_bottleneck)
        )
        
        return {
            'selected_action': best_action.value,
            'target_bottleneck': target_bid,
            'bottleneck_type': target_bottleneck.type.value,
            'expected_impact': self._estimate_impact(best_action, target_bottleneck)
        }
    
    def _calculate_action_score(
        self, 
        action: EvolutionAction, 
        bottleneck: Bottleneck
    ) -> float:
        """计算行动得分"""
        strategy = self.evolution_strategies[action]
        
        # 风险调整收益
        risk_adjusted_reward = strategy['reward'] * (1 - strategy['risk'])
        
        # 瓶颈严重程度加成
        severity_bonus = bottleneck.severity * 0.3
        
        return risk_adjusted_reward + severity_bonus - strategy['cost']
    
    def _estimate_impact(
        self, 
        action: EvolutionAction, 
        bottleneck: Bottleneck
    ) -> float:
        """估计影响"""
        strategy = self.evolution_strategies[action]
        return strategy['reward'] * bottleneck.severity
    
    def _execute_evolution(
        self, 
        action: str, 
        target_bottleneck_id: str
    ) -> Dict:
        """执行演化"""
        action_enum = EvolutionAction(action)
        target_bottleneck = self.bottlenecks[target_bottleneck_id]
        
        # 创建演化事件
        event = EvolutionEvent(
            id=f"evo_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            from_version=self.current_state.version,
            to_version=self._increment_version(action_enum),
            action=action_enum,
            description=f"执行{action_enum.value}以解决{target_bottleneck.type.value}瓶颈",
            trigger=f"瓶颈: {target_bottleneck.description}",
            changes={},
            capabilities_added=[],
            capabilities_improved=[],
            connections_established=[],
            impact_score=0,
            success=False,
            lessons_learned=[]
        )
        
        # 执行具体的演化行动
        execution_result = self._apply_evolution_action(action_enum, target_bottleneck)
        
        event.changes = execution_result.get('changes', {})
        event.capabilities_added = execution_result.get('capabilities_added', [])
        event.capabilities_improved = execution_result.get('capabilities_improved', [])
        event.connections_established = execution_result.get('connections_established', [])
        event.impact_score = execution_result.get('impact_score', 0)
        event.success = execution_result.get('success', False)
        event.lessons_learned = execution_result.get('lessons_learned', [])
        
        # 更新版本
        self.current_state.version = event.to_version
        
        # 记录事件
        self.evolution_chain.add_event(event)
        self.stats['total_evolutions'] += 1
        
        if event.success and event.impact_score > 0.7:
            self.stats['total_breakthroughs'] += 1
            self.evolution_chain.total_breakthroughs += 1
        
        return {
            'event_id': event.id,
            'action': action,
            'success': event.success,
            'impact': event.impact_score,
            'new_version': event.to_version
        }
    
    def _increment_version(self, action: EvolutionAction) -> str:
        """递增版本号"""
        parts = self.current_state.version.replace('v', '').split('.')
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        
        # 根据行动类型决定版本递增幅度
        if action == EvolutionAction.RESTRUCTURE:
            major += 1
            minor = 0
            patch = 0
        elif action in [EvolutionAction.EXTEND, EvolutionAction.EMERGE]:
            minor += 1
        else:
            patch += 1
        
        return f"v{major}.{minor}.{patch}"
    
    def _apply_evolution_action(
        self, 
        action: EvolutionAction, 
        bottleneck: Bottleneck
    ) -> Dict:
        """应用演化行动"""
        result = {
            'changes': {},
            'capabilities_added': [],
            'capabilities_improved': [],
            'connections_established': [],
            'impact_score': 0,
            'success': False,
            'lessons_learned': []
        }
        
        # 更新瓶颈解决进度
        progress_increase = random.uniform(0.1, 0.4)
        bottleneck.resolution_progress = min(1.0, bottleneck.resolution_progress + progress_increase)
        
        if action == EvolutionAction.EXTEND:
            result.update(self._action_extend(bottleneck))
        elif action == EvolutionAction.DEEPEN:
            result.update(self._action_deepen(bottleneck))
        elif action == EvolutionAction.CONNECT:
            result.update(self._action_connect(bottleneck))
        elif action == EvolutionAction.RESTRUCTURE:
            result.update(self._action_restructure(bottleneck))
        elif action == EvolutionAction.OPTIMIZE:
            result.update(self._action_optimize(bottleneck))
        elif action == EvolutionAction.EMERGE:
            result.update(self._action_emerge(bottleneck))
        
        # 更新认知维度
        if result['success']:
            dimension_updates = self._get_dimension_updates(action, bottleneck)
            for dim, delta in dimension_updates.items():
                current_value = getattr(self.current_state, dim, 0.5)
                setattr(self.current_state, dim, min(1, current_value + delta))
            
            result['impact_score'] = sum(dimension_updates.values()) / len(dimension_updates)
        
        return result
    
    def _action_extend(self, bottleneck: Bottleneck) -> Dict:
        """扩展行动"""
        new_capability = f"新能力_{datetime.now().strftime('%H%M%S')}"
        return {
            'capabilities_added': [new_capability],
            'changes': {'extended': True},
            'success': True,
            'lessons_learned': ["扩展需要持续投入"]
        }
    
    def _action_deepen(self, bottleneck: Bottleneck) -> Dict:
        """深化行动"""
        return {
            'capabilities_improved': [bottleneck.type.value],
            'changes': {'deepened': True},
            'success': True,
            'lessons_learned': ["深化需要反复练习"]
        }
    
    def _action_connect(self, bottleneck: Bottleneck) -> Dict:
        """连接行动"""
        return {
            'connections_established': [f"连接_{datetime.now().strftime('%H%M%S')}"],
            'changes': {'connected': True},
            'success': True,
            'lessons_learned': ["跨领域连接带来创新"]
        }
    
    def _action_restructure(self, bottleneck: Bottleneck) -> Dict:
        """重构行动"""
        return {
            'changes': {'restructured': True, 'architecture': 'upgraded'},
            'success': random.random() > 0.3,  # 重构有风险
            'lessons_learned': ["重构需要勇气"]
        }
    
    def _action_optimize(self, bottleneck: Bottleneck) -> Dict:
        """优化行动"""
        return {
            'changes': {'optimized': True, 'efficiency': 'improved'},
            'success': True,
            'lessons_learned': ["持续优化是常态"]
        }
    
    def _action_emerge(self, bottleneck: Bottleneck) -> Dict:
        """涌现行动"""
        new_capability = f"涌现能力_{datetime.now().strftime('%H%M%S')}"
        return {
            'capabilities_added': [new_capability],
            'changes': {'emerged': True},
            'success': random.random() > 0.4,  # 涌现有不确定性
            'lessons_learned': ["涌现需要条件成熟"]
        }
    
    def _get_dimension_updates(
        self, 
        action: EvolutionAction, 
        bottleneck: Bottleneck
    ) -> Dict[str, float]:
        """获取维度更新"""
        base_updates = {
            EvolutionAction.EXTEND: {
                'knowledge_breadth': 0.1,
                'capability_level': 0.05
            },
            EvolutionAction.DEEPEN: {
                'knowledge_depth': 0.1,
                'capability_level': 0.08
            },
            EvolutionAction.CONNECT: {
                'connectivity_score': 0.15,
                'creativity_score': 0.05
            },
            EvolutionAction.RESTRUCTURE: {
                'integration_score': 0.15,
                'adaptability_score': 0.1
            },
            EvolutionAction.OPTIMIZE: {
                'integration_score': 0.08,
                'stability_score': 0.05
            },
            EvolutionAction.EMERGE: {
                'creativity_score': 0.15,
                'capability_level': 0.1
            }
        }
        
        return base_updates.get(action, {})
    
    def _evaluate_evolution_effect(self, evolution_result: Dict) -> Dict:
        """评估演化效果"""
        if evolution_result.get('success'):
            # 更新成长率
            growth_rate = evolution_result.get('impact', 0)
            self.current_state.growth_rate = (
                self.current_state.growth_rate * 0.7 + growth_rate * 0.3
            )
            
            # 检查是否需要更新阶段
            if growth_rate > 0.5:
                self.current_state.phase = EvolutionPhase.BREAKTHROUGH
            elif growth_rate > 0.2:
                self.current_state.phase = EvolutionPhase.GROWTH
        
        return {
            'current_phase': self.current_state.phase.value,
            'growth_rate': self.current_state.growth_rate,
            'active_bottlenecks': len(self.current_state.active_bottlenecks)
        }
    
    def _update_cognitive_state(self, cycle_result: Dict) -> None:
        """更新认知状态"""
        self.current_state.timestamp = datetime.now().isoformat()
        
        # 更新稳定性
        if self.current_state.active_bottlenecks:
            self.current_state.stability_score = max(0, 1 - len(self.current_state.active_bottlenecks) * 0.1)
        else:
            self.current_state.stability_score = 1.0
    
    # ==================== 外部接口 ====================
    
    def get_evolution_report(self) -> Dict:
        """获取演化报告"""
        return {
            'current_state': {
                'version': self.current_state.version,
                'phase': self.current_state.phase.value,
                'dimensions': {
                    'knowledge_depth': self.current_state.knowledge_depth,
                    'knowledge_breadth': self.current_state.knowledge_breadth,
                    'capability_level': self.current_state.capability_level,
                    'connectivity_score': self.current_state.connectivity_score,
                    'creativity_score': self.current_state.creativity_score,
                    'integration_score': self.current_state.integration_score
                },
                'active_bottlenecks': len(self.current_state.active_bottlenecks),
                'growth_rate': self.current_state.growth_rate
            },
            'evolution_stats': {
                'total_evolutions': self.evolution_chain.total_evolutions,
                'successful_evolutions': self.evolution_chain.successful_evolutions,
                'breakthroughs': self.evolution_chain.total_breakthroughs,
                'capabilities_gained': self.evolution_chain.total_capabilities_gained
            },
            'bottleneck_stats': {
                'total_identified': self.stats['total_bottlenecks_identified'],
                'total_resolved': self.stats['total_bottlenecks_resolved'],
                'currently_active': len([b for b in self.bottlenecks.values() if not b.resolved_time])
            }
        }
    
    def get_evolution_history(self, limit: int = 10) -> List[Dict]:
        """获取演化历史"""
        events = self.evolution_chain.events[-limit:]
        return [{
            'id': e.id,
            'timestamp': e.timestamp,
            'action': e.action.value,
            'description': e.description,
            'success': e.success,
            'impact': e.impact_score,
            'from_version': e.from_version,
            'to_version': e.to_version
        } for e in events]
    
    def get_active_bottlenecks(self) -> List[Dict]:
        """获取活跃瓶颈"""
        return [{
            'id': b.id,
            'type': b.type.value,
            'description': b.description,
            'severity': b.severity,
            'progress': b.resolution_progress,
            'solutions': b.potential_solutions[:3]
        } for b in self.bottlenecks.values() if not b.resolved_time]
    
    def _load_state(self) -> None:
        """加载状态"""
        state_file = os.path.join(self.storage_path, 'evolution_state.json')
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)
                
                self.stats = data.get('stats', self.stats)
                
                # 加载认知状态
                if 'current_state' in data:
                    cs = data['current_state']
                    self.current_state = CognitiveState(
                        timestamp=cs.get('timestamp', datetime.now().isoformat()),
                        version=cs.get('version', 'v1.0.0'),
                        phase=EvolutionPhase(cs.get('phase', 'stable')),
                        knowledge_depth=cs.get('knowledge_depth', 0.5),
                        knowledge_breadth=cs.get('knowledge_breadth', 0.5),
                        capability_level=cs.get('capability_level', 0.5),
                        connectivity_score=cs.get('connectivity_score', 0.5),
                        creativity_score=cs.get('creativity_score', 0.5),
                        integration_score=cs.get('integration_score', 0.5),
                        active_bottlenecks=cs.get('active_bottlenecks', []),
                        bottleneck_severity=cs.get('bottleneck_severity', 0),
                        growth_rate=cs.get('growth_rate', 0),
                        stability_score=cs.get('stability_score', 1.0),
                        adaptability_score=cs.get('adaptability_score', 0.5)
                    )
                
                # 加载瓶颈
                for bid, b_data in data.get('bottlenecks', {}).items():
                    self.bottlenecks[bid] = Bottleneck(
                        id=b_data['id'],
                        type=BottleneckType(b_data['type']),
                        description=b_data['description'],
                        severity=b_data['severity'],
                        impact=b_data.get('impact', []),
                        root_cause=b_data.get('root_cause', ''),
                        potential_solutions=b_data.get('potential_solutions', []),
                        resolution_progress=b_data.get('resolution_progress', 0),
                        discovered_time=b_data['discovered_time'],
                        resolved_time=b_data.get('resolved_time')
                    )
            except Exception as e:
                print(f"加载状态失败: {e}")
    
    def _save_state(self) -> None:
        """保存状态"""
        state_file = os.path.join(self.storage_path, 'evolution_state.json')
        
        data = {
            'stats': self.stats,
            'current_state': {
                'timestamp': self.current_state.timestamp,
                'version': self.current_state.version,
                'phase': self.current_state.phase.value,
                'knowledge_depth': self.current_state.knowledge_depth,
                'knowledge_breadth': self.current_state.knowledge_breadth,
                'capability_level': self.current_state.capability_level,
                'connectivity_score': self.current_state.connectivity_score,
                'creativity_score': self.current_state.creativity_score,
                'integration_score': self.current_state.integration_score,
                'active_bottlenecks': self.current_state.active_bottlenecks,
                'bottleneck_severity': self.current_state.bottleneck_severity,
                'growth_rate': self.current_state.growth_rate,
                'stability_score': self.current_state.stability_score,
                'adaptability_score': self.current_state.adaptability_score
            },
            'bottlenecks': {bid: {
                'id': b.id,
                'type': b.type.value,
                'description': b.description,
                'severity': b.severity,
                'impact': b.impact,
                'root_cause': b.root_cause,
                'potential_solutions': b.potential_solutions,
                'resolution_progress': b.resolution_progress,
                'discovered_time': b.discovered_time,
                'resolved_time': b.resolved_time
            } for bid, b in self.bottlenecks.items()}
        }
        
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)


def demo_evolution():
    """演示自进化内核"""
    print("=" * 60)
    print("自进化内核演示")
    print("=" * 60)
    
    core = SelfEvolutionCore()
    
    print(f"\n初始认知状态:")
    print(f"  版本: {core.current_state.version}")
    print(f"  阶段: {core.current_state.phase.value}")
    print(f"  知识深度: {core.current_state.knowledge_depth:.2f}")
    print(f"  能力水平: {core.current_state.capability_level:.2f}")
    
    # 执行几个进化循环
    print("\n执行进化循环...")
    for i in range(3):
        print(f"\n--- 循环 {i+1} ---")
        result = core.evolve_cycle()
        
        assessment = result['stages'].get('self_assessment', {})
        print(f"自评估: 总分={assessment.get('overall_score', 0):.2f}")
        print(f"  弱点: {assessment.get('weaknesses', [])}")
        
        bottleneck = result['stages'].get('bottleneck_analysis', {})
        print(f"瓶颈分析: 关键瓶颈数={len(bottleneck.get('critical_bottlenecks', []))}")
        
        evolution = result['stages'].get('evolution_result', {})
        if evolution:
            print(f"演化: 行动={evolution.get('action')}, 成功={evolution.get('success')}")
            print(f"  新版本: {evolution.get('new_version')}")
    
    # 查看演化报告
    print("\n演化报告:")
    report = core.get_evolution_report()
    print(f"  当前版本: {report['current_state']['version']}")
    print(f"  当前阶段: {report['current_state']['phase']}")
    print(f"  总演化次数: {report['evolution_stats']['total_evolutions']}")
    print(f"  突破次数: {report['evolution_stats']['breakthroughs']}")


if __name__ == "__main__":
    demo_evolution()
