#!/usr/bin/env python3
"""
细胞休眠与唤醒系统
基于神经科学的记忆激活理论：记忆永不消失，只是休眠

核心理念:
- 永不遗忘：记忆细胞永远存在
- 休眠状态：低能量、高唤醒阈值
- 唤醒机制：特定刺激可以唤醒休眠细胞
- 能量分配：活跃记忆获得更多能量
"""

import json
import math
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import random


class CellState(Enum):
    """细胞状态"""
    HYPER_ACTIVE = "hyper_active"    # 超活跃：刚被强烈激活
    ACTIVE = "active"                # 活跃：正常工作状态
    DORMANT = "dormant"              # 休眠：低能量，可唤醒
    DEEP_DORMANT = "deep_dormant"    # 深度休眠：极低能量，需要强刺激唤醒
    CRYO = "cryo"                    # 冷冻：几乎无能量，需要极强刺激


@dataclass
class CellEnergy:
    """细胞能量系统"""
    current: float = 1.0           # 当前能量 [0, 2]
    base_rate: float = 0.1         # 基础衰减率
    activation_threshold: float = 0.3  # 激活阈值
    wake_boost: float = 0.5        # 唤醒能量增益
    
    def decay(self, time_elapsed: float, importance: float = 0.5) -> None:
        """能量衰减（艾宾浩斯启发）"""
        # 衰减因子：重要性越高，衰减越慢
        decay_factor = 1.0 - (importance * 0.5)
        
        # 时间衰减（对数曲线）
        time_factor = math.log(1 + time_elapsed) / 10.0
        
        # 综合衰减
        self.current *= math.exp(-self.base_rate * time_factor * decay_factor)
        self.current = max(0.01, self.current)  # 最低保留
    
    def activate(self, boost: float = 0.3) -> None:
        """激活（能量增加）"""
        self.current = min(2.0, self.current + boost)
    
    def is_active(self) -> bool:
        """是否处于活跃状态"""
        return self.current >= self.activation_threshold


@dataclass
class WakeTrigger:
    """唤醒触发器"""
    trigger_type: str              # 触发类型: semantic, emotional, temporal, association
    keywords: List[str]            # 关键词
    min_intensity: float = 0.5     # 最小刺激强度
    energy_boost: float = 0.5      # 唤醒后能量增益
    
    def matches(self, stimulus: Dict) -> Tuple[bool, float]:
        """检查是否匹配刺激"""
        intensity = 0.0
        
        # 语义匹配
        if self.trigger_type == "semantic":
            stimulus_text = stimulus.get('text', '').lower()
            for keyword in self.keywords:
                if keyword.lower() in stimulus_text:
                    intensity += 0.3
        
        # 情感匹配
        elif self.trigger_type == "emotional":
            stimulus_emotion = stimulus.get('emotion', {})
            for emotion in self.keywords:
                if emotion in stimulus_emotion:
                    intensity += stimulus_emotion[emotion] * 0.5
        
        # 时间匹配
        elif self.trigger_type == "temporal":
            stimulus_time = stimulus.get('time', {})
            for time_pattern in self.keywords:
                if time_pattern in str(stimulus_time):
                    intensity += 0.4
        
        # 关联匹配
        elif self.trigger_type == "association":
            stimulus_associations = stimulus.get('associations', set())
            for assoc in self.keywords:
                if assoc in stimulus_associations:
                    intensity += 0.35
        
        matched = intensity >= self.min_intensity
        return matched, intensity


class DormancySystem:
    """
    休眠系统
    
    管理细胞的休眠、唤醒、能量分配
    """
    
    def __init__(self, storage_path: str = "./memory/dormancy"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        # 细胞状态注册表
        self.cell_states: Dict[str, CellState] = {}
        self.cell_energy: Dict[str, CellEnergy] = {}
        self.wake_triggers: Dict[str, List[WakeTrigger]] = {}
        
        # 状态转换统计
        self.stats = {
            'total_dormant': 0,
            'total_deep_dormant': 0,
            'total_cryo': 0,
            'wake_events': 0,
            'sleep_events': 0
        }
        
        self._load_state()
    
    def register_cell(self, cell_id: str, initial_energy: float = 1.0,
                      wake_triggers: List[WakeTrigger] = None) -> None:
        """注册细胞到休眠系统"""
        self.cell_states[cell_id] = CellState.ACTIVE
        self.cell_energy[cell_id] = CellEnergy(current=initial_energy)
        self.wake_triggers[cell_id] = wake_triggers or []
    
    def update_cell_state(self, cell_id: str, energy: float = None,
                          time_elapsed: float = 0, importance: float = 0.5) -> CellState:
        """更新细胞状态"""
        if cell_id not in self.cell_energy:
            self.register_cell(cell_id)
        
        energy_system = self.cell_energy[cell_id]
        
        if energy is not None:
            energy_system.current = energy
        else:
            energy_system.decay(time_elapsed, importance)
        
        # 根据能量确定状态
        old_state = self.cell_states[cell_id]
        new_state = self._determine_state(energy_system.current)
        self.cell_states[cell_id] = new_state
        
        # 更新统计
        if old_state != new_state:
            if new_state in [CellState.DORMANT, CellState.DEEP_DORMANT, CellState.CRYO]:
                self.stats['sleep_events'] += 1
            if old_state in [CellState.DORMANT, CellState.DEEP_DORMANT, CellState.CRYO]:
                self.stats['wake_events'] += 1
        
        self._update_stats()
        return new_state
    
    def _determine_state(self, energy: float) -> CellState:
        """根据能量确定状态"""
        if energy >= 1.5:
            return CellState.HYPER_ACTIVE
        elif energy >= 0.5:
            return CellState.ACTIVE
        elif energy >= 0.2:
            return CellState.DORMANT
        elif energy >= 0.05:
            return CellState.DEEP_DORMANT
        else:
            return CellState.CRYO
    
    def activate_cell(self, cell_id: str, intensity: float = 0.3) -> bool:
        """激活细胞"""
        if cell_id not in self.cell_energy:
            return False
        
        old_state = self.cell_states[cell_id]
        
        # 根据当前状态决定激活难度
        if old_state == CellState.CRYO:
            intensity *= 0.3  # 冷冻状态需要更强刺激
        elif old_state == CellState.DEEP_DORMANT:
            intensity *= 0.5  # 深度休眠需要较强刺激
        elif old_state == CellState.DORMANT:
            intensity *= 0.8  # 休眠状态正常激活
        
        self.cell_energy[cell_id].activate(intensity)
        
        # 更新状态
        new_energy = self.cell_energy[cell_id].current
        new_state = self._determine_state(new_energy)
        self.cell_states[cell_id] = new_state
        
        # 唤醒计数
        if old_state in [CellState.DORMANT, CellState.DEEP_DORMANT, CellState.CRYO]:
            if new_state in [CellState.ACTIVE, CellState.HYPER_ACTIVE]:
                self.stats['wake_events'] += 1
        
        self._update_stats()
        return new_state in [CellState.ACTIVE, CellState.HYPER_ACTIVE]
    
    def check_wake_triggers(self, cell_id: str, stimulus: Dict) -> Tuple[bool, float]:
        """检查唤醒触发器"""
        if cell_id not in self.wake_triggers:
            return False, 0.0
        
        max_intensity = 0.0
        any_matched = False
        
        for trigger in self.wake_triggers[cell_id]:
            matched, intensity = trigger.matches(stimulus)
            if matched:
                any_matched = True
                max_intensity = max(max_intensity, intensity)
        
        return any_matched, max_intensity
    
    def process_stimulus(self, stimulus: Dict, all_cell_ids: List[str]) -> List[Tuple[str, float]]:
        """
        处理刺激，返回应该被唤醒的细胞
        
        Returns:
            [(cell_id, wake_intensity), ...]
        """
        wake_list = []
        
        for cell_id in all_cell_ids:
            state = self.cell_states.get(cell_id, CellState.ACTIVE)
            
            # 只检查休眠中的细胞
            if state in [CellState.DORMANT, CellState.DEEP_DORMANT, CellState.CRYO]:
                matched, intensity = self.check_wake_triggers(cell_id, stimulus)
                
                if matched:
                    wake_list.append((cell_id, intensity))
        
        # 按强度排序
        wake_list.sort(key=lambda x: -x[1])
        return wake_list
    
    def energy_allocation(self, total_energy: float = 100.0) -> Dict[str, float]:
        """
        能量分配算法
        
        根据细胞状态和重要性分配能量
        活跃细胞获得更多能量，休眠细胞获得基本维持能量
        """
        allocation = {}
        
        # 计算各状态细胞数量和权重
        state_weights = {
            CellState.HYPER_ACTIVE: 3.0,
            CellState.ACTIVE: 2.0,
            CellState.DORMANT: 0.5,
            CellState.DEEP_DORMANT: 0.1,
            CellState.CRYO: 0.01
        }
        
        total_weight = 0.0
        for cell_id, state in self.cell_states.items():
            total_weight += state_weights[state]
        
        if total_weight == 0:
            return allocation
        
        # 分配能量
        for cell_id, state in self.cell_states.items():
            weight = state_weights[state]
            allocation[cell_id] = (weight / total_weight) * total_energy
        
        return allocation
    
    def get_active_cells(self) -> List[str]:
        """获取所有活跃细胞"""
        return [cid for cid, state in self.cell_states.items()
                if state in [CellState.ACTIVE, CellState.HYPER_ACTIVE]]
    
    def get_dormant_cells(self) -> List[str]:
        """获取所有休眠细胞"""
        return [cid for cid, state in self.cell_states.items()
                if state in [CellState.DORMANT, CellState.DEEP_DORMANT, CellState.CRYO]]
    
    def get_cells_by_state(self, state: CellState) -> List[str]:
        """按状态获取细胞"""
        return [cid for cid, s in self.cell_states.items() if s == state]
    
    def _update_stats(self) -> None:
        """更新统计信息"""
        self.stats['total_dormant'] = len(self.get_cells_by_state(CellState.DORMANT))
        self.stats['total_deep_dormant'] = len(self.get_cells_by_state(CellState.DEEP_DORMANT))
        self.stats['total_cryo'] = len(self.get_cells_by_state(CellState.CRYO))
    
    def get_state_distribution(self) -> Dict[str, int]:
        """获取状态分布"""
        distribution = {state.value: 0 for state in CellState}
        for state in self.cell_states.values():
            distribution[state.value] += 1
        return distribution
    
    def add_wake_trigger(self, cell_id: str, trigger: WakeTrigger) -> None:
        """添加唤醒触发器"""
        if cell_id not in self.wake_triggers:
            self.wake_triggers[cell_id] = []
        self.wake_triggers[cell_id].append(trigger)
    
    def _load_state(self) -> None:
        """加载状态"""
        state_file = os.path.join(self.storage_path, 'dormancy_state.json')
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)
                
                self.cell_states = {
                    k: CellState(v) for k, v in data.get('cell_states', {}).items()
                }
                self.cell_energy = {
                    k: CellEnergy(**v) for k, v in data.get('cell_energy', {}).items()
                }
                self.stats = data.get('stats', self.stats)
            except Exception:
                pass
    
    def save_state(self) -> None:
        """保存状态"""
        state_file = os.path.join(self.storage_path, 'dormancy_state.json')
        
        data = {
            'cell_states': {k: v.value for k, v in self.cell_states.items()},
            'cell_energy': {k: {'current': v.current, 'base_rate': v.base_rate,
                               'activation_threshold': v.activation_threshold,
                               'wake_boost': v.wake_boost}
                          for k, v in self.cell_energy.items()},
            'stats': self.stats
        }
        
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_report(self) -> Dict:
        """获取系统报告"""
        return {
            'total_cells': len(self.cell_states),
            'state_distribution': self.get_state_distribution(),
            'active_count': len(self.get_active_cells()),
            'dormant_count': len(self.get_dormant_cells()),
            'wake_events': self.stats['wake_events'],
            'sleep_events': self.stats['sleep_events'],
            'average_energy': sum(e.current for e in self.cell_energy.values()) / max(1, len(self.cell_energy))
        }


def demo_dormancy():
    """演示休眠系统"""
    print("=" * 60)
    print("细胞休眠与唤醒系统演示")
    print("=" * 60)
    
    system = DormancySystem()
    
    # 注册细胞
    cells = [
        ("cell_001", ["python", "开发", "代码"]),
        ("cell_002", ["用户", "偏好", "设置"]),
        ("cell_003", ["项目", "任务", "进度"]),
        ("cell_004", ["会议", "讨论", "决策"]),
        ("cell_005", ["重要", "紧急", "优先"])
    ]
    
    print("\n注册细胞...")
    for cell_id, keywords in cells:
        trigger = WakeTrigger(
            trigger_type="semantic",
            keywords=keywords,
            min_intensity=0.3
        )
        system.register_cell(cell_id, wake_triggers=[trigger])
    
    # 模拟时间流逝，细胞进入休眠
    print("\n模拟时间流逝（30天）...")
    for cell_id, _ in cells:
        state = system.update_cell_state(cell_id, time_elapsed=30, importance=0.3)
        print(f"  {cell_id}: {state.value}")
    
    # 查看状态分布
    print(f"\n状态分布: {system.get_state_distribution()}")
    
    # 模拟刺激唤醒
    print("\n模拟刺激: '用户正在进行Python项目开发'...")
    stimulus = {
        'text': '用户正在进行Python项目开发',
        'type': 'semantic'
    }
    
    wake_list = system.process_stimulus(stimulus, [c[0] for c in cells])
    print(f"应唤醒细胞: {wake_list}")
    
    # 执行唤醒
    for cell_id, intensity in wake_list:
        success = system.activate_cell(cell_id, intensity * 0.5)
        print(f"  唤醒 {cell_id}: {'成功' if success else '失败'}")
    
    # 查看报告
    print(f"\n系统报告:")
    report = system.get_report()
    for k, v in report.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    demo_dormancy()
