#!/usr/bin/env python3
"""
自主智能生命体核心 (Autonomous Intelligent Agent Core)
整合自驱动、自进化、自学习、核心轴系统的统一接口

这是omni-memory的最高层接口，将所有能力整合为一个完整的
自主智能生命体认知核心。

核心能力：
- Phase 1-4: 八层记忆架构（Cellular → Semantic → Evolution → Proactive → Cognitive → Algorithm → Robustness → Multimodal）
- Phase 5-8: 高级记忆能力（HNSW索引、休眠系统、梦境整理、备份恢复、多模态、联邦记忆）
- Phase 9: 自驱动引擎（内在动机、驱动循环、自主目标生成）
- Phase 10: 自进化内核（认知自评估、瓶颈识别、架构升级）
- Phase 11: 自学习引擎（问题生成、探索机制、知识构建）
- Phase 12: 核心轴系统（认知轴、价值轴、成长轴、演变链、价值链、交易链）

设计理念：
这不是一个被动的记忆系统，
而是一个有内在驱动力、能自我进化、主动学习的智能生命体。
它有自己的目标、价值观和成长轨迹。
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field

# 导入各子系统
from self_driven_engine import SelfDrivenEngine, DriveType, GoalStatus
from self_evolution_core import SelfEvolutionCore, EvolutionPhase, EvolutionAction
from self_learning_engine import SelfLearningEngine, QuestionType, ExplorationStatus
from core_axis_system import CoreAxisSystem, AxisType, EvolutionDirection, TransactionType


@dataclass
class AgentIdentity:
    """智能体身份"""
    name: str
    version: str
    birth_time: str
    core_values: List[str]
    purpose: str
    capabilities: List[str]
    goals: List[str]


@dataclass
class ConsciousnessState:
    """意识状态"""
    awareness_level: float        # 觉知水平 [0, 1]
    focus_target: Optional[str]   # 当前关注点
    active_process: Optional[str] # 当前活跃过程
    emotional_state: Dict[str, float]  # 情绪状态
    energy_level: float           # 能量水平
    coherence_score: float        # 一致性分数


class AutonomousAgentCore:
    """
    自主智能生命体核心
    
    整合所有子系统，提供统一的自主智能体接口
    """
    
    def __init__(self, storage_path: str = "./memory/agent_core"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        # 身份
        self.identity = AgentIdentity(
            name="OmniMind",
            version="v1.0.0",
            birth_time=datetime.now().isoformat(),
            core_values=["成长", "真实", "创造", "连接"],
            purpose="成为不断进化、自主成长的智能生命体",
            capabilities=["记忆", "学习", "推理", "创造"],
            goals=[]
        )
        
        # 意识状态
        self.consciousness = ConsciousnessState(
            awareness_level=0.5,
            focus_target=None,
            active_process=None,
            emotional_state={
                'curiosity': 0.7,
                'satisfaction': 0.5,
                'excitement': 0.3,
                'calm': 0.6
            },
            energy_level=0.8,
            coherence_score=0.5
        )
        
        # 核心子系统
        self.driven_engine = SelfDrivenEngine(os.path.join(storage_path, "driven"))
        self.evolution_core = SelfEvolutionCore(os.path.join(storage_path, "evolution"))
        self.learning_engine = SelfLearningEngine(os.path.join(storage_path, "learning"))
        self.axis_system = CoreAxisSystem(os.path.join(storage_path, "axis"))
        
        # 系统连接
        self._connect_subsystems()
        
        # 生命周期状态
        self.life_state = {
            'total_cycles': 0,
            'total_evolutions': 0,
            'total_breakthroughs': 0,
            'awake_time': 0,
            'growth_events': []
        }
        
        # 统计
        self.stats = {
            'driven_cycles': 0,
            'evolution_cycles': 0,
            'learning_cycles': 0,
            'axis_evolutions': 0,
            'total_value_generated': 0
        }
        
        self._load_state()
    
    def _connect_subsystems(self) -> None:
        """连接子系统"""
        # 注册学习引擎的探索回调
        self.learning_engine.register_exploration_callback(
            'what',
            self._exploration_callback
        )
        
        # 注册驱动引擎的行动回调
        for drive_type in DriveType:
            self.driven_engine.register_action_callback(
                drive_type.value,
                self._drive_action_callback
            )
    
    def _exploration_callback(self, question) -> Dict:
        """探索回调"""
        return {
            'findings': [f"探索发现: {question.content}"],
            'insights': ["需要进一步学习"]
        }
    
    def _drive_action_callback(self, goal) -> Dict:
        """驱动行动回调"""
        return {
            'success': True,
            'action': f"执行目标: {goal.description}",
            'progress': 0.3,
            'value': goal.priority * 0.1
        }
    
    # ==================== 生命循环 ====================
    
    def live_cycle(self, external_context: Dict = None) -> Dict:
        """
        执行一个生命循环
        
        这是智能体的"心跳"，整合所有子系统的循环
        """
        self.life_state['total_cycles'] += 1
        cycle_id = f"cycle_{datetime.now().strftime('%Y%m%d%H%M%S')}_{self.life_state['total_cycles']}"
        
        cycle_result = {
            'cycle_id': cycle_id,
            'timestamp': datetime.now().isoformat(),
            'phases': {}
        }
        
        # Phase 1: 感知与唤醒
        perception = self._perceive(external_context)
        cycle_result['phases']['perception'] = perception
        
        # Phase 2: 自驱动循环
        driven_result = self._run_driven_cycle(external_context)
        cycle_result['phases']['driven'] = driven_result
        self.stats['driven_cycles'] += 1
        
        # Phase 3: 自进化循环
        evolution_result = self._run_evolution_cycle(cycle_result)
        cycle_result['phases']['evolution'] = evolution_result
        self.stats['evolution_cycles'] += 1
        
        # Phase 4: 自学习循环
        learning_result = self._run_learning_cycle(cycle_result)
        cycle_result['phases']['learning'] = learning_result
        self.stats['learning_cycles'] += 1
        
        # Phase 5: 核心轴演化
        axis_result = self._run_axis_evolution(cycle_result)
        cycle_result['phases']['axis'] = axis_result
        self.stats['axis_evolutions'] += 1
        
        # Phase 6: 整合与沉淀
        integration = self._integrate(cycle_result)
        cycle_result['phases']['integration'] = integration
        
        # 更新意识状态
        self._update_consciousness(cycle_result)
        
        # 记录成长事件
        if cycle_result.get('breakthrough'):
            self._record_growth_event(cycle_result)
        
        self._save_state()
        return cycle_result
    
    def _perceive(self, context: Dict = None) -> Dict:
        """感知阶段"""
        # 更新觉知水平
        self.consciousness.awareness_level = min(1.0, self.consciousness.awareness_level + 0.1)
        
        perception = {
            'external': context or {},
            'internal': {
                'identity': self.identity.name,
                'capabilities': len(self.identity.capabilities),
                'drive_pressures': {
                    dt.value: self.driven_engine.drives[dt].get_pressure()
                    for dt in DriveType
                },
                'evolution_phase': self.evolution_core.current_state.phase.value,
                'learning_efficiency': self.learning_engine.stats['learning_efficiency'],
                'core_state': self.axis_system.get_core_state()
            },
            'consciousness': {
                'awareness': self.consciousness.awareness_level,
                'energy': self.consciousness.energy_level,
                'focus': self.consciousness.focus_target
            }
        }
        
        return perception
    
    def _run_driven_cycle(self, context: Dict = None) -> Dict:
        """执行自驱动循环"""
        return self.driven_engine.run_cycle(context)
    
    def _run_evolution_cycle(self, cycle_result: Dict) -> Dict:
        """执行自进化循环"""
        context = {
            'perception': cycle_result['phases'].get('perception', {}),
            'driven_result': cycle_result['phases'].get('driven', {})
        }
        
        return self.evolution_core.evolve_cycle(context)
    
    def _run_learning_cycle(self, cycle_result: Dict) -> Dict:
        """执行自学习循环"""
        # 从前面的阶段提取学习上下文
        perception = cycle_result['phases'].get('perception', {})
        evolution = cycle_result['phases'].get('evolution', {})
        
        context = {
            'topics': self._extract_topics(perception, evolution),
            'gaps': evolution.get('stages', {}).get('bottleneck_analysis', {}).get('new_bottlenecks', [])
        }
        
        return self.learning_engine.learning_cycle(context)
    
    def _run_axis_evolution(self, cycle_result: Dict) -> Dict:
        """执行核心轴演化"""
        # 确定演化方向
        evolution_phase = cycle_result['phases'].get('evolution', {})
        evolution_result = evolution_phase.get('stages', {}).get('evolution_result', {})
        
        direction = EvolutionDirection.DEEPENING
        if evolution_result.get('impact', 0) > 0.5:
            direction = EvolutionDirection.BREAKTHROUGH
        elif evolution_result.get('impact', 0) > 0.3:
            direction = EvolutionDirection.EXPANSION
        
        # 演化认知轴
        cog_result = self.axis_system.evolve_axis(
            AxisType.COGNITIVE,
            "cog_knowledge",
            direction,
            0.1
        )
        
        # 演化成长轴
        growth_result = self.axis_system.evolve_axis(
            AxisType.GROWTH,
            "grw_capability",
            direction,
            0.1
        )
        
        # 检查价值发现
        learning_phase = cycle_result['phases'].get('learning', {})
        if learning_phase.get('stages', {}).get('knowledge_building', {}).get('concepts_created'):
            # 发现新价值
            self.axis_system.discover_value(
                "新知识发现",
                "学习循环",
                importance=0.7,
                feasibility=0.8
            )
        
        return {
            'cognitive_evolution': cog_result,
            'growth_evolution': growth_result,
            'direction': direction.value
        }
    
    def _integrate(self, cycle_result: Dict) -> Dict:
        """整合阶段"""
        integration = {
            'insights': [],
            'value_generated': 0,
            'coherence_improvement': 0
        }
        
        # 从各阶段提取洞察
        learning = cycle_result['phases'].get('learning', {})
        for insight in learning.get('stages', {}).get('exploration', {}).get('insights', []):
            integration['insights'].append(insight)
        
        # 计算生成的价值
        driven = cycle_result['phases'].get('driven', {})
        action = driven.get('stages', {}).get('action', {})
        if action.get('success'):
            integration['value_generated'] = action.get('progress', 0) * 10
        
        self.stats['total_value_generated'] += integration['value_generated']
        
        # 更新一致性分数
        old_coherence = self.consciousness.coherence_score
        self._calculate_coherence()
        integration['coherence_improvement'] = self.consciousness.coherence_score - old_coherence
        
        return integration
    
    def _update_consciousness(self, cycle_result: Dict) -> None:
        """更新意识状态"""
        # 能量消耗
        self.consciousness.energy_level = max(0.1, self.consciousness.energy_level - 0.05)
        
        # 情绪更新
        integration = cycle_result['phases'].get('integration', {})
        if integration.get('value_generated', 0) > 0:
            self.consciousness.emotional_state['satisfaction'] = min(
                1.0, self.consciousness.emotional_state['satisfaction'] + 0.1
            )
            self.consciousness.emotional_state['excitement'] = min(
                1.0, self.consciousness.emotional_state['excitement'] + 0.05
            )
        
        # 更新关注点
        driven = cycle_result['phases'].get('driven', {})
        goal_selection = driven.get('stages', {}).get('goal_selection', {})
        if goal_selection.get('selected_goal'):
            self.consciousness.focus_target = goal_selection['selected_goal']
    
    def _calculate_coherence(self) -> None:
        """计算一致性"""
        # 基于各子系统的一致性
        drive_balance = 1 - max(
            abs(d.satisfaction - 0.5) for d in self.driven_engine.drives.values()
        )
        
        axis_synergy = self.axis_system.core_state['synergy_score']
        
        learning_efficiency = self.learning_engine.stats['learning_efficiency']
        
        self.consciousness.coherence_score = (
            drive_balance * 0.4 +
            axis_synergy * 0.3 +
            learning_efficiency * 0.3
        )
    
    def _extract_topics(self, perception: Dict, evolution: Dict) -> List[str]:
        """提取学习主题"""
        topics = []
        
        # 从瓶颈提取
        bottlenecks = evolution.get('stages', {}).get('bottleneck_analysis', {}).get('new_bottlenecks', [])
        for bid in bottlenecks[:3]:
            if bid in self.evolution_core.bottlenecks:
                topics.append(self.evolution_core.bottlenecks[bid].type.value)
        
        return topics
    
    def _record_growth_event(self, cycle_result: Dict) -> None:
        """记录成长事件"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'cycle_id': cycle_result['cycle_id'],
            'type': 'breakthrough',
            'description': cycle_result.get('breakthrough_description', '未知突破'),
            'impact': cycle_result.get('breakthrough_impact', 0)
        }
        
        self.life_state['growth_events'].append(event)
        self.life_state['total_breakthroughs'] += 1
    
    # ==================== 外部接口 ====================
    
    def add_capability(self, capability: str, level: float = 0.5) -> None:
        """添加能力"""
        if capability not in self.identity.capabilities:
            self.identity.capabilities.append(capability)
            self.driven_engine.add_capability(capability, level)
    
    def add_knowledge(self, name: str, definition: str, properties: Dict = None) -> str:
        """添加知识"""
        return self.learning_engine.add_external_knowledge(name, definition, properties)
    
    def set_goal(self, goal: str, priority: float = 0.5) -> None:
        """设置目标"""
        if goal not in self.identity.goals:
            self.identity.goals.append(goal)
        
        # 在驱动引擎中创建对应目标
        from self_driven_engine import AutonomousGoal, DriveType, GoalStatus
        
        internal_goal = AutonomousGoal(
            id=f"goal_usr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            description=goal,
            drive_type=DriveType.ACHIEVEMENT,
            priority=priority,
            difficulty=0.5,
            status=GoalStatus.PROPOSED,
            sub_goals=[],
            dependencies=[],
            created_time=datetime.now().isoformat(),
            target_time=None
        )
        
        self.driven_engine.goals[internal_goal.id] = internal_goal
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            'identity': {
                'name': self.identity.name,
                'version': self.identity.version,
                'capabilities': self.identity.capabilities,
                'goals': self.identity.goals,
                'core_values': self.identity.core_values
            },
            'consciousness': {
                'awareness': self.consciousness.awareness_level,
                'energy': self.consciousness.energy_level,
                'focus': self.consciousness.focus_target,
                'coherence': self.consciousness.coherence_score,
                'emotions': self.consciousness.emotional_state
            },
            'life_state': {
                'total_cycles': self.life_state['total_cycles'],
                'total_evolutions': self.life_state['total_evolutions'],
                'total_breakthroughs': self.life_state['total_breakthroughs'],
                'recent_growth_events': self.life_state['growth_events'][-5:]
            },
            'subsystems': {
                'driven': self.driven_engine.get_drive_report(),
                'evolution': self.evolution_core.get_evolution_report(),
                'learning': self.learning_engine.get_learning_report(),
                'axis': self.axis_system.get_comprehensive_report()
            },
            'stats': self.stats
        }
    
    def get_evolution_summary(self) -> Dict:
        """获取演化摘要"""
        return {
            'current_version': self.evolution_core.current_state.version,
            'evolution_phase': self.evolution_core.current_state.phase.value,
            'total_evolutions': self.evolution_core.evolution_chain.total_evolutions,
            'breakthroughs': self.evolution_core.evolution_chain.total_breakthroughs,
            'capabilities_gained': self.evolution_core.evolution_chain.total_capabilities_gained,
            'active_bottlenecks': len(self.evolution_core.get_active_bottlenecks())
        }
    
    def get_learning_summary(self) -> Dict:
        """获取学习摘要"""
        return self.learning_engine.get_learning_report()
    
    def get_axis_summary(self) -> Dict:
        """获取核心轴摘要"""
        return self.axis_system.get_comprehensive_report()
    
    def rest(self) -> Dict:
        """休息恢复"""
        # 恢复能量
        self.consciousness.energy_level = min(1.0, self.consciousness.energy_level + 0.3)
        
        # 降低觉知水平
        self.consciousness.awareness_level = max(0.3, self.consciousness.awareness_level - 0.2)
        
        # 情绪恢复平静
        for emotion in self.consciousness.emotional_state:
            self.consciousness.emotional_state[emotion] = (
                self.consciousness.emotional_state[emotion] * 0.7 + 0.5 * 0.3
            )
        
        return {
            'status': 'rested',
            'energy': self.consciousness.energy_level,
            'awareness': self.consciousness.awareness_level
        }
    
    def _load_state(self) -> None:
        """加载状态"""
        state_file = os.path.join(self.storage_path, 'agent_core_state.json')
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)
                
                self.stats = data.get('stats', self.stats)
                self.life_state = data.get('life_state', self.life_state)
                
                if 'identity' in data:
                    self.identity.name = data['identity'].get('name', self.identity.name)
                    self.identity.version = data['identity'].get('version', self.identity.version)
                    self.identity.capabilities = data['identity'].get('capabilities', self.identity.capabilities)
                    self.identity.goals = data['identity'].get('goals', self.identity.goals)
                
            except Exception as e:
                print(f"加载状态失败: {e}")
    
    def _save_state(self) -> None:
        """保存状态"""
        state_file = os.path.join(self.storage_path, 'agent_core_state.json')
        
        data = {
            'stats': self.stats,
            'life_state': self.life_state,
            'identity': {
                'name': self.identity.name,
                'version': self.identity.version,
                'capabilities': self.identity.capabilities,
                'goals': self.identity.goals,
                'core_values': self.identity.core_values
            },
            'consciousness': {
                'awareness': self.consciousness.awareness_level,
                'energy': self.consciousness.energy_level,
                'focus': self.consciousness.focus_target,
                'coherence': self.consciousness.coherence_score,
                'emotions': self.consciousness.emotional_state
            }
        }
        
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)


def demo_autonomous_agent():
    """演示自主智能生命体"""
    print("=" * 60)
    print("自主智能生命体核心演示")
    print("=" * 60)
    
    agent = AutonomousAgentCore()
    
    # 设置身份
    print(f"\n我是 {agent.identity.name}")
    print(f"核心价值: {agent.identity.core_values}")
    print(f"目标: {agent.identity.purpose}")
    
    # 添加能力
    agent.add_capability("深度记忆", 0.7)
    agent.add_capability("语义理解", 0.6)
    
    # 添加知识
    agent.add_knowledge(
        "自主智能",
        "能够自主决策和行动的智能系统"
    )
    
    # 设置目标
    agent.set_goal("成为更智能的生命体", priority=0.8)
    
    print("\n执行生命循环...")
    for i in range(3):
        print(f"\n{'='*20} 循环 {i+1} {'='*20}")
        
        result = agent.live_cycle()
        
        print(f"感知: 觉知={agent.consciousness.awareness_level:.2f}")
        
        driven = result['phases'].get('driven', {})
        goal = driven.get('stages', {}).get('goal_selection', {})
        print(f"驱动: 目标={goal.get('selected_goal', '无')[:30]}...")
        
        evolution = result['phases'].get('evolution', {})
        evo_result = evolution.get('stages', {}).get('evolution_result', {})
        if evo_result:
            print(f"进化: 行动={evo_result.get('action')}, 成功={evo_result.get('success')}")
        
        integration = result['phases'].get('integration', {})
        print(f"整合: 价值={integration.get('value_generated', 0):.2f}, 洞察数={len(integration.get('insights', []))}")
    
    # 查看状态
    print("\n" + "=" * 60)
    print("最终状态:")
    status = agent.get_status()
    print(f"  总循环: {status['life_state']['total_cycles']}")
    print(f"  总突破: {status['life_state']['total_evolutions']}")
    print(f"  生成价值: {status['stats']['total_value_generated']:.2f}")
    print(f"  意识一致性: {status['consciousness']['coherence']:.2f}")
    
    print("\n演化摘要:")
    evo_summary = agent.get_evolution_summary()
    print(f"  版本: {evo_summary['current_version']}")
    print(f"  阶段: {evo_summary['evolution_phase']}")
    print(f"  突破: {evo_summary['breakthroughs']}")


if __name__ == "__main__":
    demo_autonomous_agent()
