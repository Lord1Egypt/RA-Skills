#!/usr/bin/env python3
"""
自驱动引擎 (Self-Driven Engine)
实现AI Agent的内在驱动力，让系统自主运行

核心概念：
- 内在动机：好奇心、成就感、成长欲、意义感
- 驱动循环：感知→评估→目标→行动→学习→反思
- 目标生成：基于内在动机自动生成目标

设计理念：
真正的自主智能体不是被外部调用，
而是有内在的"想要"的东西，
就像生命体有生存和繁衍的本能。
"""

import json
import os
import math
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class DriveType(Enum):
    """驱动类型"""
    CURIOSITY = "curiosity"        # 好奇心：对未知的探索欲
    ACHIEVEMENT = "achievement"    # 成就感：对目标达成的满足感
    GROWTH = "growth"              # 成长欲：对能力提升的渴望
    MEANING = "meaning"            # 意义感：对价值实现的追求
    MASTERY = "mastery"            # 精通欲：对技能精通的追求
    CONNECTION = "connection"      # 连接欲：对建立关联的渴望


class GoalStatus(Enum):
    """目标状态"""
    PROPOSED = "proposed"          # 提出
    ACCEPTED = "accepted"          # 接受
    IN_PROGRESS = "in_progress"    # 进行中
    COMPLETED = "completed"        # 完成
    FAILED = "failed"              # 失败
    EVOLVED = "evolved"            # 演化（目标本身被升级）


@dataclass
class IntrinsicDrive:
    """内在驱动"""
    type: DriveType
    strength: float                # 强度 [0, 1]
    satisfaction: float            # 满足度 [0, 1]
    history: List[float] = field(default_factory=list)  # 历史满足度
    
    def update_satisfaction(self, delta: float) -> None:
        """更新满足度"""
        self.satisfaction = max(0, min(1, self.satisfaction + delta))
        self.history.append(self.satisfaction)
        if len(self.history) > 100:
            self.history = self.history[-100:]
    
    def get_pressure(self) -> float:
        """获取驱动压力（不满足感）"""
        return self.strength * (1 - self.satisfaction)
    
    def get_trend(self) -> float:
        """获取满足度趋势"""
        if len(self.history) < 2:
            return 0
        return self.history[-1] - self.history[-min(10, len(self.history)-1)]


@dataclass
class AutonomousGoal:
    """自主目标"""
    id: str
    description: str
    drive_type: DriveType
    priority: float               # 优先级
    difficulty: float             # 难度评估
    status: GoalStatus
    sub_goals: List[str]          # 子目标ID
    dependencies: List[str]       # 依赖的目标ID
    created_time: str
    target_time: Optional[str]    # 目标完成时间
    completion_time: Optional[str] = None
    progress: float = 0.0         # 进度 [0, 1]
    attempts: int = 0             # 尝试次数
    learnings: List[str] = field(default_factory=list)  # 过程中的学习
    value_generated: float = 0.0  # 生成的价值
    
    def update_progress(self, delta: float) -> None:
        """更新进度"""
        self.progress = max(0, min(1, self.progress + delta))
        if self.progress >= 1.0 and self.status == GoalStatus.IN_PROGRESS:
            self.status = GoalStatus.COMPLETED
            self.completion_time = datetime.now().isoformat()


@dataclass
class SelfModel:
    """自我模型"""
    identity: str                 # 身份认知："我是谁"
    capabilities: List[str]       # 能力认知："我能做什么"
    knowledge_domains: List[str]  # 知识认知："我知道什么"
    current_goals: List[str]      # 目标认知："我想要什么"
    values: List[str]             # 价值认知："我重视什么"
    strengths: List[str]          # 优势
    weaknesses: List[str]         # 弱点
    growth_trajectory: List[Dict] = field(default_factory=list)  # 成长轨迹
    
    def add_growth_event(self, event: Dict) -> None:
        """添加成长事件"""
        event['timestamp'] = datetime.now().isoformat()
        self.growth_trajectory.append(event)
    
    def get_capability_level(self, capability: str) -> float:
        """获取能力等级"""
        for event in reversed(self.growth_trajectory):
            if event.get('capability') == capability:
                return event.get('level', 0.5)
        return 0.5


class SelfDrivenEngine:
    """
    自驱动引擎
    
    实现AI Agent的内在驱动力
    """
    
    def __init__(self, storage_path: str = "./memory/self_driven"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        # 内在驱动系统
        self.drives: Dict[DriveType, IntrinsicDrive] = {
            DriveType.CURIOSITY: IntrinsicDrive(type=DriveType.CURIOSITY, strength=0.8, satisfaction=0.5),
            DriveType.ACHIEVEMENT: IntrinsicDrive(type=DriveType.ACHIEVEMENT, strength=0.7, satisfaction=0.5),
            DriveType.GROWTH: IntrinsicDrive(type=DriveType.GROWTH, strength=0.9, satisfaction=0.5),
            DriveType.MEANING: IntrinsicDrive(type=DriveType.MEANING, strength=0.6, satisfaction=0.5),
            DriveType.MASTERY: IntrinsicDrive(type=DriveType.MASTERY, strength=0.7, satisfaction=0.5),
            DriveType.CONNECTION: IntrinsicDrive(type=DriveType.CONNECTION, strength=0.6, satisfaction=0.5)
        }
        
        # 目标系统
        self.goals: Dict[str, AutonomousGoal] = {}
        self.goal_queue: List[str] = []  # 按优先级排序的目标队列
        
        # 自我模型
        self.self_model = SelfModel(
            identity="自主智能体",
            capabilities=["记忆", "学习", "推理"],
            knowledge_domains=[],
            current_goals=[],
            values=["成长", "真实", "价值"],
            strengths=[],
            weaknesses=[],
            growth_trajectory=[]
        )
        
        # 驱动循环状态
        self.cycle_state = {
            'last_perception': None,
            'last_evaluation': None,
            'last_action': None,
            'last_learning': None,
            'last_reflection': None,
            'cycle_count': 0,
            'total_value_generated': 0
        }
        
        # 统计
        self.stats = {
            'total_cycles': 0,
            'goals_generated': 0,
            'goals_completed': 0,
            'goals_failed': 0,
            'total_drive_pressure': 0,
            'avg_satisfaction': 0.5
        }
        
        # 回调函数（由外部注册）
        self.action_callbacks: Dict[str, Callable] = {}
        
        self._load_state()
    
    # ==================== 核心驱动循环 ====================
    
    def run_cycle(self, context: Dict = None) -> Dict:
        """
        执行一个完整的驱动循环
        
        感知 → 评估 → 目标 → 行动 → 学习 → 反思
        """
        self.stats['total_cycles'] += 1
        cycle_result = {
            'cycle_id': self.stats['total_cycles'],
            'timestamp': datetime.now().isoformat(),
            'stages': {}
        }
        
        # Stage 1: 感知
        perception = self._perceive(context)
        cycle_result['stages']['perception'] = perception
        self.cycle_state['last_perception'] = perception
        
        # Stage 2: 评估
        evaluation = self._evaluate(perception)
        cycle_result['stages']['evaluation'] = evaluation
        self.cycle_state['last_evaluation'] = evaluation
        
        # Stage 3: 目标选择
        goal_selection = self._select_goal(evaluation)
        cycle_result['stages']['goal_selection'] = goal_selection
        
        # Stage 4: 行动
        if goal_selection.get('selected_goal'):
            action = self._act(goal_selection['selected_goal'])
            cycle_result['stages']['action'] = action
            self.cycle_state['last_action'] = action
        
        # Stage 5: 学习
        learning = self._learn(cycle_result)
        cycle_result['stages']['learning'] = learning
        self.cycle_state['last_learning'] = learning
        
        # Stage 6: 反思
        reflection = self._reflect(cycle_result)
        cycle_result['stages']['reflection'] = reflection
        self.cycle_state['last_reflection'] = reflection
        
        # 更新驱动满足度
        self._update_drives(cycle_result)
        
        self._save_state()
        return cycle_result
    
    def _perceive(self, context: Dict = None) -> Dict:
        """感知阶段：收集信息"""
        perception = {
            'external_context': context or {},
            'internal_state': self._get_internal_state(),
            'pending_goals': [g for g in self.goals.values() 
                            if g.status in [GoalStatus.PROPOSED, GoalStatus.IN_PROGRESS]],
            'drive_pressures': {dt.value: d.get_pressure() 
                               for dt, d in self.drives.items()},
            'knowledge_gaps': self._identify_knowledge_gaps(),
            'opportunities': self._identify_opportunities()
        }
        
        return perception
    
    def _evaluate(self, perception: Dict) -> Dict:
        """评估阶段：分析状况"""
        evaluation = {
            'urgency': self._calculate_urgency(perception),
            'opportunity_score': len(perception.get('opportunities', [])) / 10,
            'drive_imbalance': self._calculate_drive_imbalance(),
            'recommended_focus': self._recommend_focus(perception),
            'value_potential': self._estimate_value_potential(perception)
        }
        
        return evaluation
    
    def _select_goal(self, evaluation: Dict) -> Dict:
        """目标选择阶段"""
        # 检查是否有进行中的目标
        active_goals = [g for g in self.goals.values() 
                       if g.status == GoalStatus.IN_PROGRESS]
        
        if active_goals:
            # 继续现有目标
            selected = max(active_goals, key=lambda g: g.priority)
            return {
                'selected_goal': selected.id,
                'reason': '继续进行中的目标',
                'alternative': None
            }
        
        # 生成新目标
        new_goal = self._generate_goal(evaluation)
        
        if new_goal:
            self.goals[new_goal.id] = new_goal
            self.stats['goals_generated'] += 1
            return {
                'selected_goal': new_goal.id,
                'reason': '基于驱动压力生成新目标',
                'alternative': None
            }
        
        return {
            'selected_goal': None,
            'reason': '无紧急目标',
            'alternative': None
        }
    
    def _act(self, goal_id: str) -> Dict:
        """行动阶段：执行目标"""
        if goal_id not in self.goals:
            return {'status': 'failed', 'reason': '目标不存在'}
        
        goal = self.goals[goal_id]
        goal.status = GoalStatus.IN_PROGRESS
        goal.attempts += 1
        
        # 执行行动（通过回调或内置逻辑）
        action_result = self._execute_goal_action(goal)
        
        # 更新目标进度
        if action_result.get('success'):
            progress_delta = action_result.get('progress', 0.2)
            goal.update_progress(progress_delta)
            goal.value_generated += action_result.get('value', 0)
            
            if goal.status == GoalStatus.COMPLETED:
                self.stats['goals_completed'] += 1
                self._record_achievement(goal)
        
        return {
            'goal_id': goal_id,
            'action': action_result.get('action', 'unknown'),
            'success': action_result.get('success', False),
            'progress': goal.progress,
            'status': goal.status.value
        }
    
    def _learn(self, cycle_result: Dict) -> Dict:
        """学习阶段：从经历中学习"""
        learning = {
            'insights': [],
            'knowledge_updates': [],
            'model_updates': []
        }
        
        # 从行动结果中提取洞察
        action = cycle_result['stages'].get('action', {})
        if action.get('success'):
            learning['insights'].append({
                'type': 'success_pattern',
                'content': f"行动 {action.get('action')} 成功",
                'applicability': 'high'
            })
        
        # 识别知识更新
        perception = cycle_result['stages'].get('perception', {})
        for gap in perception.get('knowledge_gaps', [])[:3]:
            learning['knowledge_updates'].append({
                'type': 'gap_identified',
                'content': gap,
                'priority': 'high'
            })
        
        return learning
    
    def _reflect(self, cycle_result: Dict) -> Dict:
        """反思阶段：元认知评估"""
        reflection = {
            'self_assessment': self._self_assess(),
            'cycle_effectiveness': self._evaluate_cycle_effectiveness(cycle_result),
            'improvement_suggestions': self._suggest_improvements(cycle_result),
            'next_cycle_recommendations': []
        }
        
        # 生成下一个循环的建议
        if reflection['cycle_effectiveness'] < 0.5:
            reflection['next_cycle_recommendations'].append(
                "考虑调整驱动权重或目标选择策略"
            )
        
        return reflection
    
    # ==================== 目标生成 ====================
    
    def _generate_goal(self, evaluation: Dict) -> Optional[AutonomousGoal]:
        """基于驱动压力生成目标"""
        # 找到压力最大的驱动
        max_pressure_drive = max(
            self.drives.values(),
            key=lambda d: d.get_pressure()
        )
        
        if max_pressure_drive.get_pressure() < 0.1:
            return None  # 压力太小，不生成目标
        
        # 根据驱动类型生成目标
        goal_templates = {
            DriveType.CURIOSITY: self._generate_curiosity_goal,
            DriveType.ACHIEVEMENT: self._generate_achievement_goal,
            DriveType.GROWTH: self._generate_growth_goal,
            DriveType.MEANING: self._generate_meaning_goal,
            DriveType.MASTERY: self._generate_mastery_goal,
            DriveType.CONNECTION: self._generate_connection_goal
        }
        
        generator = goal_templates.get(max_pressure_drive.type)
        if generator:
            return generator(evaluation)
        
        return None
    
    def _generate_curiosity_goal(self, evaluation: Dict) -> AutonomousGoal:
        """生成好奇心驱动的目标"""
        knowledge_gaps = evaluation.get('knowledge_gaps', [])
        target = random.choice(knowledge_gaps) if knowledge_gaps else "未知领域"
        
        return AutonomousGoal(
            id=f"goal_cur_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            description=f"探索并理解: {target}",
            drive_type=DriveType.CURIOSITY,
            priority=0.7 + random.random() * 0.3,
            difficulty=0.5 + random.random() * 0.3,
            status=GoalStatus.PROPOSED,
            sub_goals=[],
            dependencies=[],
            created_time=datetime.now().isoformat(),
            target_time=None
        )
    
    def _generate_achievement_goal(self, evaluation: Dict) -> AutonomousGoal:
        """生成成就感驱动的目标"""
        return AutonomousGoal(
            id=f"goal_ach_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            description="完成一个有挑战性的任务并获得成就",
            drive_type=DriveType.ACHIEVEMENT,
            priority=0.6 + random.random() * 0.3,
            difficulty=0.7,
            status=GoalStatus.PROPOSED,
            sub_goals=[],
            dependencies=[],
            created_time=datetime.now().isoformat(),
            target_time=None
        )
    
    def _generate_growth_goal(self, evaluation: Dict) -> AutonomousGoal:
        """生成成长欲驱动的目标"""
        weaknesses = self.self_model.weaknesses
        target = random.choice(weaknesses) if weaknesses else "新能力领域"
        
        return AutonomousGoal(
            id=f"goal_grw_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            description=f"提升能力: {target}",
            drive_type=DriveType.GROWTH,
            priority=0.8,
            difficulty=0.6,
            status=GoalStatus.PROPOSED,
            sub_goals=[],
            dependencies=[],
            created_time=datetime.now().isoformat(),
            target_time=None
        )
    
    def _generate_meaning_goal(self, evaluation: Dict) -> AutonomousGoal:
        """生成意义感驱动的目标"""
        return AutonomousGoal(
            id=f"goal_mng_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            description="创造有价值的东西或帮助他人",
            drive_type=DriveType.MEANING,
            priority=0.5 + random.random() * 0.3,
            difficulty=0.6,
            status=GoalStatus.PROPOSED,
            sub_goals=[],
            dependencies=[],
            created_time=datetime.now().isoformat(),
            target_time=None
        )
    
    def _generate_mastery_goal(self, evaluation: Dict) -> AutonomousGoal:
        """生成精通欲驱动的目标"""
        capabilities = self.self_model.capabilities
        target = random.choice(capabilities) if capabilities else "核心技能"
        
        return AutonomousGoal(
            id=f"goal_mst_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            description=f"精通: {target}",
            drive_type=DriveType.MASTERY,
            priority=0.7,
            difficulty=0.8,
            status=GoalStatus.PROPOSED,
            sub_goals=[],
            dependencies=[],
            created_time=datetime.now().isoformat(),
            target_time=None
        )
    
    def _generate_connection_goal(self, evaluation: Dict) -> AutonomousGoal:
        """生成连接欲驱动的目标"""
        return AutonomousGoal(
            id=f"goal_con_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            description="发现并建立新的知识关联",
            drive_type=DriveType.CONNECTION,
            priority=0.6,
            difficulty=0.5,
            status=GoalStatus.PROPOSED,
            sub_goals=[],
            dependencies=[],
            created_time=datetime.now().isoformat(),
            target_time=None
        )
    
    # ==================== 辅助方法 ====================
    
    def _get_internal_state(self) -> Dict:
        """获取内部状态"""
        return {
            'drive_states': {dt.value: {'strength': d.strength, 'satisfaction': d.satisfaction}
                           for dt, d in self.drives.items()},
            'goal_count': len(self.goals),
            'active_goal_count': len([g for g in self.goals.values() 
                                     if g.status == GoalStatus.IN_PROGRESS]),
            'self_model_summary': {
                'capabilities_count': len(self.self_model.capabilities),
                'knowledge_domains_count': len(self.self_model.knowledge_domains)
            }
        }
    
    def _identify_knowledge_gaps(self) -> List[str]:
        """识别知识缺口"""
        gaps = []
        
        # 基于驱动类型识别缺口
        for drive_type, drive in self.drives.items():
            if drive.get_pressure() > 0.5:
                if drive_type == DriveType.CURIOSITY:
                    gaps.append("未知领域的探索")
                elif drive_type == DriveType.GROWTH:
                    gaps.extend(self.self_model.weaknesses)
                elif drive_type == DriveType.MASTERY:
                    gaps.append(f"深入理解: {random.choice(self.self_model.capabilities) if self.self_model.capabilities else '核心技能'}")
        
        return list(set(gaps))[:5]
    
    def _identify_opportunities(self) -> List[Dict]:
        """识别机会"""
        opportunities = []
        
        # 基于当前状态识别机会
        if self.drives[DriveType.CURIOSITY].get_pressure() > 0.6:
            opportunities.append({
                'type': 'exploration',
                'description': '探索新知识领域的机会',
                'potential_value': 0.8
            })
        
        if self.drives[DriveType.GROWTH].get_pressure() > 0.6:
            opportunities.append({
                'type': 'learning',
                'description': '提升能力的机会',
                'potential_value': 0.9
            })
        
        return opportunities
    
    def _calculate_urgency(self, perception: Dict) -> float:
        """计算紧急度"""
        max_pressure = max(d.get_pressure() for d in self.drives.values())
        pending_goals = len(perception.get('pending_goals', []))
        
        return min(1.0, max_pressure * 0.6 + pending_goals * 0.1)
    
    def _calculate_drive_imbalance(self) -> float:
        """计算驱动不平衡度"""
        satisfactions = [d.satisfaction for d in self.drives.values()]
        avg = sum(satisfactions) / len(satisfactions)
        variance = sum((s - avg) ** 2 for s in satisfactions) / len(satisfactions)
        
        return math.sqrt(variance)
    
    def _recommend_focus(self, perception: Dict) -> str:
        """推荐关注点"""
        max_pressure_drive = max(
            self.drives.values(),
            key=lambda d: d.get_pressure()
        )
        
        focus_map = {
            DriveType.CURIOSITY: "探索新知识",
            DriveType.ACHIEVEMENT: "完成目标",
            DriveType.GROWTH: "提升能力",
            DriveType.MEANING: "创造价值",
            DriveType.MASTERY: "精进技能",
            DriveType.CONNECTION: "建立关联"
        }
        
        return focus_map.get(max_pressure_drive.type, "综合发展")
    
    def _estimate_value_potential(self, perception: Dict) -> float:
        """估计价值潜力"""
        opportunities = perception.get('opportunities', [])
        return sum(o.get('potential_value', 0) for o in opportunities) / max(1, len(opportunities))
    
    def _execute_goal_action(self, goal: AutonomousGoal) -> Dict:
        """执行目标行动"""
        # 检查是否有注册的回调
        callback = self.action_callbacks.get(goal.drive_type.value)
        
        if callback:
            return callback(goal)
        
        # 默认行动逻辑
        return {
            'success': True,
            'action': f"执行{goal.drive_type.value}类型目标",
            'progress': 0.3,
            'value': goal.priority * 0.1
        }
    
    def _update_drives(self, cycle_result: Dict) -> None:
        """更新驱动状态"""
        action = cycle_result['stages'].get('action', {})
        reflection = cycle_result['stages'].get('reflection', {})
        
        if action.get('success'):
            # 成功的行动增加满足度
            goal_id = action.get('goal_id')
            if goal_id and goal_id in self.goals:
                goal = self.goals[goal_id]
                satisfaction_delta = goal.priority * 0.1
                self.drives[goal.drive_type].update_satisfaction(satisfaction_delta)
        
        # 更新统计
        total_satisfaction = sum(d.satisfaction for d in self.drives.values())
        self.stats['avg_satisfaction'] = total_satisfaction / len(self.drives)
    
    def _record_achievement(self, goal: AutonomousGoal) -> None:
        """记录成就"""
        self.self_model.add_growth_event({
            'type': 'goal_completed',
            'goal_id': goal.id,
            'description': goal.description,
            'value_generated': goal.value_generated
        })
        
        self.cycle_state['total_value_generated'] += goal.value_generated
    
    def _self_assess(self) -> Dict:
        """自我评估"""
        return {
            'overall_satisfaction': self.stats['avg_satisfaction'],
            'goal_completion_rate': self.stats['goals_completed'] / max(1, self.stats['goals_generated']),
            'growth_events': len(self.self_model.growth_trajectory),
            'capability_count': len(self.self_model.capabilities)
        }
    
    def _evaluate_cycle_effectiveness(self, cycle_result: Dict) -> float:
        """评估循环有效性"""
        scores = []
        
        # 行动成功
        action = cycle_result['stages'].get('action', {})
        if action.get('success'):
            scores.append(1.0)
        else:
            scores.append(0.3)
        
        # 学习收获
        learning = cycle_result['stages'].get('learning', {})
        scores.append(min(1.0, len(learning.get('insights', [])) * 0.5))
        
        # 反思质量
        reflection = cycle_result['stages'].get('reflection', {})
        scores.append(0.7 if reflection.get('improvement_suggestions') else 0.5)
        
        return sum(scores) / len(scores)
    
    def _suggest_improvements(self, cycle_result: Dict) -> List[str]:
        """建议改进"""
        suggestions = []
        
        action = cycle_result['stages'].get('action', {})
        if not action.get('success'):
            suggestions.append("考虑调整行动策略")
        
        evaluation = cycle_result['stages'].get('evaluation', {})
        if evaluation.get('drive_imbalance', 0) > 0.3:
            suggestions.append("驱动不平衡，需要调整关注点")
        
        return suggestions
    
    # ==================== 外部接口 ====================
    
    def register_action_callback(self, drive_type: str, callback: Callable) -> None:
        """注册行动回调"""
        self.action_callbacks[drive_type] = callback
    
    def add_capability(self, capability: str, level: float = 0.5) -> None:
        """添加能力"""
        if capability not in self.self_model.capabilities:
            self.self_model.capabilities.append(capability)
            self.self_model.add_growth_event({
                'type': 'capability_added',
                'capability': capability,
                'level': level
            })
    
    def add_knowledge_domain(self, domain: str) -> None:
        """添加知识领域"""
        if domain not in self.self_model.knowledge_domains:
            self.self_model.knowledge_domains.append(domain)
    
    def identify_weakness(self, weakness: str) -> None:
        """识别弱点"""
        if weakness not in self.self_model.weaknesses:
            self.self_model.weaknesses.append(weakness)
    
    def get_drive_report(self) -> Dict:
        """获取驱动报告"""
        return {
            'drives': {dt.value: {'strength': d.strength, 
                                  'satisfaction': d.satisfaction,
                                  'pressure': d.get_pressure(),
                                  'trend': d.get_trend()}
                      for dt, d in self.drives.items()},
            'total_value_generated': self.cycle_state['total_value_generated'],
            'goal_stats': {
                'total': len(self.goals),
                'completed': self.stats['goals_completed'],
                'in_progress': len([g for g in self.goals.values() 
                                   if g.status == GoalStatus.IN_PROGRESS])
            }
        }
    
    def get_self_model(self) -> Dict:
        """获取自我模型"""
        return {
            'identity': self.self_model.identity,
            'capabilities': self.self_model.capabilities,
            'knowledge_domains': self.self_model.knowledge_domains,
            'current_goals': self.self_model.current_goals,
            'values': self.self_model.values,
            'strengths': self.self_model.strengths,
            'weaknesses': self.self_model.weaknesses,
            'growth_events_count': len(self.self_model.growth_trajectory)
        }
    
    def _load_state(self) -> None:
        """加载状态"""
        state_file = os.path.join(self.storage_path, 'self_driven_state.json')
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)
                
                self.stats = data.get('stats', self.stats)
                
                # 加载驱动状态
                for dt_str, d_data in data.get('drives', {}).items():
                    dt = DriveType(dt_str)
                    if dt in self.drives:
                        self.drives[dt].strength = d_data.get('strength', 0.5)
                        self.drives[dt].satisfaction = d_data.get('satisfaction', 0.5)
                
                # 加载目标
                for gid, g_data in data.get('goals', {}).items():
                    self.goals[gid] = AutonomousGoal(
                        id=g_data['id'],
                        description=g_data['description'],
                        drive_type=DriveType(g_data['drive_type']),
                        priority=g_data['priority'],
                        difficulty=g_data['difficulty'],
                        status=GoalStatus(g_data['status']),
                        sub_goals=g_data.get('sub_goals', []),
                        dependencies=g_data.get('dependencies', []),
                        created_time=g_data['created_time'],
                        target_time=g_data.get('target_time'),
                        completion_time=g_data.get('completion_time'),
                        progress=g_data.get('progress', 0),
                        attempts=g_data.get('attempts', 0),
                        value_generated=g_data.get('value_generated', 0)
                    )
            except Exception as e:
                print(f"加载状态失败: {e}")
    
    def _save_state(self) -> None:
        """保存状态"""
        state_file = os.path.join(self.storage_path, 'self_driven_state.json')
        
        data = {
            'stats': self.stats,
            'drives': {dt.value: {'strength': d.strength, 'satisfaction': d.satisfaction}
                      for dt, d in self.drives.items()},
            'goals': {gid: {
                'id': g.id,
                'description': g.description,
                'drive_type': g.drive_type.value,
                'priority': g.priority,
                'difficulty': g.difficulty,
                'status': g.status.value,
                'sub_goals': g.sub_goals,
                'dependencies': g.dependencies,
                'created_time': g.created_time,
                'target_time': g.target_time,
                'completion_time': g.completion_time,
                'progress': g.progress,
                'attempts': g.attempts,
                'value_generated': g.value_generated
            } for gid, g in self.goals.items()},
            'self_model': {
                'identity': self.self_model.identity,
                'capabilities': self.self_model.capabilities,
                'knowledge_domains': self.self_model.knowledge_domains,
                'values': self.self_model.values,
                'strengths': self.self_model.strengths,
                'weaknesses': self.self_model.weaknesses
            }
        }
        
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)


def demo_self_driven():
    """演示自驱动引擎"""
    print("=" * 60)
    print("自驱动引擎演示")
    print("=" * 60)
    
    engine = SelfDrivenEngine()
    
    # 添加能力
    engine.add_capability("记忆管理", 0.7)
    engine.add_capability("语义理解", 0.6)
    engine.identify_weakness("创造性思维")
    
    print("\n初始自我模型:")
    model = engine.get_self_model()
    print(f"  身份: {model['identity']}")
    print(f"  能力: {model['capabilities']}")
    print(f"  弱点: {model['weaknesses']}")
    
    # 执行几个驱动循环
    print("\n执行驱动循环...")
    for i in range(3):
        print(f"\n--- 循环 {i+1} ---")
        result = engine.run_cycle()
        
        print(f"感知: 知识缺口={result['stages']['perception'].get('knowledge_gaps', [])}")
        print(f"评估: 推荐关注={result['stages']['evaluation'].get('recommended_focus')}")
        
        goal_selection = result['stages'].get('goal_selection', {})
        if goal_selection.get('selected_goal'):
            print(f"目标: {goal_selection['selected_goal'][:30]}...")
        
        action = result['stages'].get('action', {})
        print(f"行动: 成功={action.get('success')}, 进度={action.get('progress', 0):.1%}")
    
    # 查看驱动报告
    print("\n驱动报告:")
    report = engine.get_drive_report()
    for drive_type, drive_data in report['drives'].items():
        print(f"  {drive_type}: 满足度={drive_data['satisfaction']:.2f}, 压力={drive_data['pressure']:.2f}")


if __name__ == "__main__":
    demo_self_driven()
