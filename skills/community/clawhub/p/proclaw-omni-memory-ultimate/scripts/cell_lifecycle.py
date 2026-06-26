#!/usr/bin/env python3
"""
Cell Lifecycle - 细胞生命周期管理
管理记忆细胞的完整生命周期：诞生、生长、分裂、休眠、唤醒
"""

import os
import sys
import json
import time
import uuid
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Set, Tuple
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum

# 导入记忆细胞和神经网络
from memory_cell import (
    MemoryCell, CellState, CellGene, Synapse, SynapseType,
    create_cell
)
from neural_network import MemoryNeuralNetwork, PulseType


class DivisionTrigger(Enum):
    """细胞分裂触发器"""
    HIGH_ENERGY = "high_energy"             # 高能量
    HIGH_ACCESS = "high_access"             # 高访问
    PATTERN_FOUND = "pattern_found"         # 发现模式
    INSIGHT_GENERATED = "insight_generated" # 生成洞察
    USER_REQUEST = "user_request"           # 用户请求


@dataclass
class DivisionResult:
    """细胞分裂结果"""
    success: bool
    parent_id: str
    child_id: Optional[str]
    child_content: str
    trigger: DivisionTrigger
    energy_transferred: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class CellLifecycleManager:
    """
    细胞生命周期管理器
    
    核心职责：
    1. 细胞诞生 - 创建新记忆细胞
    2. 细胞生长 - 能量积累与状态提升
    3. 细胞分裂 - 生发新的高价值记忆
    4. 细胞休眠 - 能量降低进入休眠
    5. 细胞唤醒 - 从休眠中激活
    6. 永恒保障 - 永不删除，结构持久化
    
    设计理念：
    - 细胞有生命力，不是静态数据
    - 永不死亡，只是沉默（深度休眠）
    - 可分裂产生新细胞
    - 形成家族谱系
    """
    
    # 生命周期参数
    DAILY_ENERGY_DECAY = 0.01           # 每日能量衰减
    ACCESS_ENERGY_BOOST = 0.1           # 访问能量增益
    PULSE_ENERGY_BOOST = 0.05           # 脉冲能量增益
    
    # 分裂参数
    SPLIT_ENERGY_THRESHOLD = 0.8        # 分裂所需能量
    SPLIT_ACCESS_THRESHOLD = 3          # 分裂所需访问次数
    SPLIT_ENERGY_COST = 0.5             # 分裂能量消耗
    CHILD_ENERGY_INHERIT = 0.3          # 子细胞能量继承比例
    
    # 休眠参数
    DORMANT_THRESHOLD = 0.5             # 休眠阈值
    HIBERNATE_THRESHOLD = 0.1           # 深度休眠阈值
    WAKE_ENERGY = 0.6                   # 唤醒时的能量
    
    # 家族限制
    MAX_GENERATIONS = 5                 # 最大代数
    MAX_CHILDREN_PER_CELL = 5           # 每个细胞最大子细胞数
    
    def __init__(self, network: MemoryNeuralNetwork):
        """
        初始化生命周期管理器
        
        Args:
            network: 记忆神经网络
        """
        self.network = network
        
        # 家族谱系
        self.lineage: Dict[str, List[str]] = defaultdict(list)  # parent_id -> [child_ids]
        self.ancestry: Dict[str, str] = {}  # cell_id -> parent_id
        
        # 分裂历史
        self.division_history: List[DivisionResult] = []
    
    def birth(self, content: str, gene: CellGene = CellGene.USER,
              importance: float = 0.7, parent_id: str = None) -> MemoryCell:
        """
        细胞诞生 - 创建新的记忆细胞
        
        Args:
            content: 记忆内容
            gene: 细胞基因类型
            importance: 重要性
            parent_id: 父细胞ID（分裂产生时）
        
        Returns:
            新创建的记忆细胞
        """
        # 创建细胞
        cell = create_cell(content, gene, importance)
        
        # 设置初始能量
        cell.energy = importance
        
        # 如果有父细胞（分裂产生）
        if parent_id:
            parent = self.network.get_cell(parent_id)
            if parent:
                cell.parent_id = parent_id
                cell.generation = parent.generation + 1
                
                # 建立谱系
                self.lineage[parent_id].append(cell.id)
                self.ancestry[cell.id] = parent_id
        
        # 加入网络
        self.network.add_cell(cell)
        
        return cell
    
    def grow(self, cell_id: str, access_type: str = "normal") -> float:
        """
        细胞生长 - 增加能量
        
        Args:
            cell_id: 细胞ID
            access_type: 访问类型 (normal/pulse/external)
        
        Returns:
            能量增益
        """
        cell = self.network.get_cell(cell_id)
        if not cell:
            return 0.0
        
        # 根据访问类型确定能量增益
        if access_type == "pulse":
            boost = cell.receive_pulse(1.0)
        else:
            boost = cell.activate(1.0)
        
        # 如果从休眠唤醒
        if cell.state == CellState.ACTIVE and cell.energy > self.DORMANT_THRESHOLD:
            pass  # 可记录唤醒事件
        
        self.network._save_network()
        return boost
    
    def can_divide(self, cell_id: str) -> Tuple[bool, DivisionTrigger]:
        """
        判断细胞是否可以分裂
        
        Args:
            cell_id: 细胞ID
        
        Returns:
            (是否可分裂, 触发原因)
        """
        cell = self.network.get_cell(cell_id)
        if not cell:
            return False, None
        
        # 检查各种分裂条件
        if cell.energy >= self.SPLIT_ENERGY_THRESHOLD:
            if cell.access_count >= self.SPLIT_ACCESS_THRESHOLD:
                return True, DivisionTrigger.HIGH_ENERGY
        
        if cell.access_count >= 5:
            return True, DivisionTrigger.HIGH_ACCESS
        
        # 检查代数限制
        if cell.generation >= self.MAX_GENERATIONS:
            return False, None
        
        # 检查子细胞数量
        if len(cell.children_ids) >= self.MAX_CHILDREN_PER_CELL:
            return False, None
        
        return False, None
    
    def divide(self, parent_id: str, child_content: str,
               child_gene: CellGene = None,
               trigger: DivisionTrigger = DivisionTrigger.HIGH_ENERGY) -> DivisionResult:
        """
        细胞分裂 - 生发新记忆
        
        Args:
            parent_id: 父细胞ID
            child_content: 子细胞内容
            child_gene: 子细胞基因（默认继承）
            trigger: 分裂触发器
        
        Returns:
            分裂结果
        """
        parent = self.network.get_cell(parent_id)
        if not parent:
            return DivisionResult(
                success=False,
                parent_id=parent_id,
                child_id=None,
                child_content=child_content,
                trigger=trigger,
                energy_transferred=0
            )
        
        # 检查分裂条件
        can_split, actual_trigger = self.can_divide(parent_id)
        if not can_split:
            return DivisionResult(
                success=False,
                parent_id=parent_id,
                child_id=None,
                child_content=child_content,
                trigger=trigger,
                energy_transferred=0
            )
        
        # 执行分裂
        child = parent.split(child_content, child_gene)
        
        if child:
            # 计算能量转移
            energy_transferred = child.energy
            
            # 加入网络
            self.network.add_cell(child)
            
            # 记录谱系
            self.lineage[parent_id].append(child.id)
            self.ancestry[child.id] = parent_id
            
            # 建立突触连接
            self.network.connect_cells(
                parent_id, child.id,
                SynapseType.HIERARCHICAL,
                strength=1.0,
                bidirectional=True
            )
            
            # 记录分裂历史
            result = DivisionResult(
                success=True,
                parent_id=parent_id,
                child_id=child.id,
                child_content=child_content,
                trigger=actual_trigger,
                energy_transferred=energy_transferred
            )
            self.division_history.append(result)
            
            return result
        
        return DivisionResult(
            success=False,
            parent_id=parent_id,
            child_id=None,
            child_content=child_content,
            trigger=trigger,
            energy_transferred=0
        )
    
    def auto_divide(self, cell_id: str) -> Optional[DivisionResult]:
        """
        自动分裂 - 基于内容分析生发新记忆
        
        当细胞满足分裂条件时，自动生成洞察型子细胞
        
        Args:
            cell_id: 细胞ID
        
        Returns:
            分裂结果，如果不满足条件返回None
        """
        can_split, trigger = self.can_divide(cell_id)
        if not can_split:
            return None
        
        cell = self.network.get_cell(cell_id)
        if not cell:
            return None
        
        # 生成洞察内容
        insight_content = self._generate_insight(cell)
        
        if not insight_content:
            return None
        
        # 执行分裂
        return self.divide(
            cell_id,
            insight_content,
            child_gene=CellGene.INSIGHT,
            trigger=trigger
        )
    
    def _generate_insight(self, cell: MemoryCell) -> Optional[str]:
        """
        从细胞内容生成洞察
        
        Args:
            cell: 源细胞
        
        Returns:
            生成的洞察内容
        """
        # 基于细胞类型和内容生成洞察
        if cell.gene == CellGene.USER:
            return f"用户偏好模式: {', '.join(cell.keywords[:3])}"
        elif cell.gene == CellGene.FEEDBACK:
            return f"反馈洞察: 重要性 {cell.importance:.1f}, 可信度 {cell.trust_score:.1f}"
        elif cell.gene == CellGene.PROJECT:
            return f"项目特征: {', '.join(cell.keywords[:3])}"
        else:
            return f"关联洞察: {', '.join(cell.keywords[:3])}"
    
    def sleep(self, cell_id: str) -> bool:
        """
        细胞休眠 - 降低能量进入休眠
        
        Args:
            cell_id: 细胞ID
        
        Returns:
            是否成功
        """
        cell = self.network.get_cell(cell_id)
        if not cell:
            return False
        
        # 能量衰减
        cell.decay(1.0)
        
        # 检查状态变化
        if cell.state in [CellState.DORMANT, CellState.HIBERNATE]:
            self.network._save_network()
            return True
        
        return False
    
    def hibernate(self, cell_id: str) -> bool:
        """
        细胞深度休眠 - 进入最小能量状态
        
        注意：永不删除，只是沉默
        
        Args:
            cell_id: 细胞ID
        
        Returns:
            是否成功
        """
        cell = self.network.get_cell(cell_id)
        if not cell:
            return False
        
        # 强制进入深度休眠
        cell.energy = 0.05
        cell.state = CellState.HIBERNATE
        
        self.network._save_network()
        return True
    
    def wake(self, cell_id: str, energy_boost: float = None) -> bool:
        """
        细胞唤醒 - 从休眠中激活
        
        Args:
            cell_id: 细胞ID
            energy_boost: 额外能量增益
        
        Returns:
            是否成功
        """
        cell = self.network.get_cell(cell_id)
        if not cell:
            return False
        
        # 唤醒
        wake_energy = energy_boost or self.WAKE_ENERGY
        cell.energy = min(1.0, cell.energy + wake_energy)
        cell.state = CellState.ACTIVE
        cell.last_active = datetime.now().isoformat()
        
        self.network._save_network()
        return True
    
    def decay_all(self, days: float = 1.0):
        """
        全网衰减 - 所有细胞能量衰减
        
        Args:
            days: 衰减天数
        """
        self.network.decay_all(days)
    
    def get_family_tree(self, cell_id: str, depth: int = 3) -> Dict:
        """
        获取细胞家族树
        
        Args:
            cell_id: 细胞ID
            depth: 树深度
        
        Returns:
            家族树结构
        """
        cell = self.network.get_cell(cell_id)
        if not cell:
            return {}
        
        tree = {
            'id': cell_id,
            'content': cell.content[:50],
            'gene': cell.gene.value,
            'energy': cell.energy,
            'generation': cell.generation,
            'parent': None,
            'children': []
        }
        
        # 父节点
        if cell.parent_id and cell.parent_id in self.network.cells:
            parent = self.network.get_cell(cell.parent_id)
            if parent:
                tree['parent'] = {
                    'id': cell.parent_id,
                    'content': parent.content[:30],
                    'gene': parent.gene.value
                }
        
        # 子节点
        for child_id in cell.children_ids:
            child = self.network.get_cell(child_id)
            if child:
                child_tree = {
                    'id': child_id,
                    'content': child.content[:30],
                    'gene': child.gene.value,
                    'energy': child.energy
                }
                tree['children'].append(child_tree)
        
        return tree
    
    def get_division_stats(self) -> Dict:
        """获取分裂统计"""
        total = len(self.division_history)
        successful = sum(1 for d in self.division_history if d.success)
        
        triggers = defaultdict(int)
        for d in self.division_history:
            triggers[d.trigger.value] += 1
        
        return {
            'total_divisions': total,
            'successful_divisions': successful,
            'success_rate': successful / total if total > 0 else 0,
            'triggers': dict(triggers)
        }
    
    def get_lifecycle_stats(self) -> Dict:
        """获取生命周期统计"""
        cells = list(self.network.cells.values())
        
        return {
            'total_cells': len(cells),
            'active_cells': sum(1 for c in cells if c.state == CellState.ACTIVE),
            'dormant_cells': sum(1 for c in cells if c.state == CellState.DORMANT),
            'hibernate_cells': sum(1 for c in cells if c.state == CellState.HIBERNATE),
            'avg_energy': sum(c.energy for c in cells) / len(cells) if cells else 0,
            'avg_age': sum(c.age for c in cells) / len(cells) if cells else 0,
            'total_families': len(self.lineage),
            'total_generations': max((c.generation for c in cells), default=0)
        }
    
    def maintain_eternal(self):
        """
        永恒维护 - 确保所有细胞永不删除
        
        核心原则：
        1. 永不删除细胞
        2. 深度休眠细胞结构完整保存
        3. 随时可以被唤醒
        """
        hibernate_cells = self.network.get_hibernate_cells()
        
        # 确保深度休眠细胞结构完整
        for cell in hibernate_cells:
            # 验证数据完整性
            assert cell.id is not None
            assert cell.content is not None
            assert cell.gene is not None
            
            # 确保可唤醒
            if cell.energy <= 0:
                cell.energy = 0.01  # 保留最小能量
        
        self.network._save_network()


def main():
    parser = argparse.ArgumentParser(description="Cell Lifecycle Manager - 细胞生命周期管理")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # birth命令
    birth_parser = subparsers.add_parser("birth", help="创建新细胞")
    birth_parser.add_argument("--content", required=True, help="记忆内容")
    birth_parser.add_argument("--type", default="user", help="细胞类型")
    birth_parser.add_argument("--importance", type=float, default=0.7, help="重要性")
    birth_parser.add_argument("--parent", help="父细胞ID")
    
    # grow命令
    grow_parser = subparsers.add_parser("grow", help="细胞生长")
    grow_parser.add_argument("--id", required=True, help="细胞ID")
    grow_parser.add_argument("--type", default="normal", help="访问类型")
    
    # divide命令
    divide_parser = subparsers.add_parser("divide", help="细胞分裂")
    divide_parser.add_argument("--parent", required=True, help="父细胞ID")
    divide_parser.add_argument("--content", required=True, help="子细胞内容")
    divide_parser.add_argument("--type", default="insight", help="子细胞类型")
    
    # wake命令
    wake_parser = subparsers.add_parser("wake", help="唤醒细胞")
    wake_parser.add_argument("--id", required=True, help="细胞ID")
    
    # sleep命令
    sleep_parser = subparsers.add_parser("sleep", help="细胞休眠")
    sleep_parser.add_argument("--id", required=True, help="细胞ID")
    
    # stats命令
    stats_parser = subparsers.add_parser("stats", help="显示统计")
    
    # family命令
    family_parser = subparsers.add_parser("family", help="显示家族树")
    family_parser.add_argument("--id", required=True, help="细胞ID")
    
    args = parser.parse_args()
    
    network = MemoryNeuralNetwork()
    lifecycle = CellLifecycleManager(network)
    
    if args.command == "birth":
        gene_map = {
            "user": CellGene.USER,
            "feedback": CellGene.FEEDBACK,
            "project": CellGene.PROJECT,
            "reference": CellGene.REFERENCE,
            "insight": CellGene.INSIGHT,
            "pattern": CellGene.PATTERN
        }
        gene = gene_map.get(args.type, CellGene.USER)
        cell = lifecycle.birth(args.content, gene, args.importance, args.parent)
        print(f"[BIRTH] Created cell: {cell.id}")
        print(json.dumps(cell.to_dict(), ensure_ascii=False, indent=2))
    
    elif args.command == "grow":
        boost = lifecycle.grow(args.id, args.type)
        print(f"[GROW] Energy boost: {boost:.3f}")
        cell = network.get_cell(args.id)
        if cell:
            print(f"Current energy: {cell.energy:.3f}, State: {cell.state.value}")
    
    elif args.command == "divide":
        gene_map = {
            "insight": CellGene.INSIGHT,
            "pattern": CellGene.PATTERN,
            "user": CellGene.USER,
            "project": CellGene.PROJECT
        }
        child_gene = gene_map.get(args.type, CellGene.INSIGHT)
        result = lifecycle.divide(args.parent, args.content, child_gene)
        print(f"[DIVIDE] Success: {result.success}")
        if result.success:
            print(f"  Child ID: {result.child_id}")
            print(f"  Energy transferred: {result.energy_transferred:.3f}")
            print(f"  Trigger: {result.trigger.value}")
    
    elif args.command == "wake":
        if lifecycle.wake(args.id):
            print(f"[WAKE] Cell {args.id} awakened")
            cell = network.get_cell(args.id)
            if cell:
                print(f"  Energy: {cell.energy:.3f}")
        else:
            print(f"[ERROR] Failed to wake cell")
    
    elif args.command == "sleep":
        if lifecycle.sleep(args.id):
            print(f"[SLEEP] Cell {args.id} is now dormant")
            cell = network.get_cell(args.id)
            if cell:
                print(f"  Energy: {cell.energy:.3f}, State: {cell.state.value}")
        else:
            print(f"[ERROR] Failed to sleep cell")
    
    elif args.command == "stats":
        stats = lifecycle.get_lifecycle_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    elif args.command == "family":
        tree = lifecycle.get_family_tree(args.id)
        print(json.dumps(tree, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    from enum import Enum
    main()
