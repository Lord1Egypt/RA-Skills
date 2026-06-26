#!/usr/bin/env python3
"""
Neural Network - 记忆神经网络
蜘蛛网式多节点多链接交叉关联网络
"""

import os
import sys
import json
import time
import uuid
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Set, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum

from memory_cell import (
    MemoryCell, CellState, CellGene, Synapse, SynapseType,
    create_cell
)


class PulseType(Enum):
    """脉冲类型"""
    ACTIVATION = "activation"       # 激活脉冲
    QUERY = "query"                 # 查询脉冲
    UPDATE = "update"               # 更新脉冲
    MEMORY = "memory"               # 记忆脉冲


@dataclass
class NeuralPulse:
    """
    神经脉冲 - 细胞间传递的信号
    
    脉冲在网络中传播，激活相关细胞
    """
    source_id: str
    target_id: str
    pulse_type: PulseType
    strength: float
    depth: int = 0
    path: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'source_id': self.source_id,
            'target_id': self.target_id,
            'pulse_type': self.pulse_type.value,
            'strength': self.strength,
            'depth': self.depth,
            'path': self.path,
            'timestamp': self.timestamp
        }


class MemoryNeuralNetwork:
    """
    记忆神经网络 - 蜘蛛网式结构
    
    核心特性：
    1. 多节点 - 每个记忆是一个节点
    2. 多链接 - 节点间多重连接
    3. 交叉关联 - 网状结构，非树状
    4. 脉冲传导 - 激活信号全网传播
    5. 自主生长 - 自动发现并建立连接
    """
    
    # 脉冲传导参数
    MAX_PULSE_DEPTH = 3             # 最大传导深度
    PULSE_DECAY_RATE = 0.5          # 每层衰减比例
    MIN_PULSE_STRENGTH = 0.05       # 最小脉冲强度
    
    # 网络生长参数
    AUTO_CONNECT_THRESHOLD = 0.7    # 自动连接阈值
    MAX_SYNAPSES_PER_CELL = 50      # 每个细胞最大突触数
    
    def __init__(self, storage_path: str = "./memory_network"):
        """
        初始化神经网络
        
        Args:
            storage_path: 存储路径
        """
        self.storage_path = storage_path
        self.cells: Dict[str, MemoryCell] = {}
        self.synapse_index: Dict[str, Set[str]] = defaultdict(set)  # 反向索引
        
        # 确保存储目录存在
        os.makedirs(storage_path, exist_ok=True)
        
        # 加载已有细胞
        self._load_network()
    
    def _load_network(self):
        """加载网络数据"""
        cells_file = os.path.join(self.storage_path, "cells.json")
        if os.path.exists(cells_file):
            try:
                with open(cells_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for cell_data in data.get('cells', []):
                        cell = MemoryCell.from_dict(cell_data)
                        self.cells[cell.id] = cell
                        
                        # 构建反向索引
                        for synapse in cell.synapses:
                            self.synapse_index[synapse.target_id].add(cell.id)
                
                print(f"[NETWORK] Loaded {len(self.cells)} cells")
            except Exception as e:
                print(f"[NETWORK] Load error: {e}")
    
    def _save_network(self):
        """保存网络数据"""
        cells_file = os.path.join(self.storage_path, "cells.json")
        try:
            data = {
                'cells': [cell.to_dict() for cell in self.cells.values()],
                'metadata': {
                    'total_cells': len(self.cells),
                    'active_cells': sum(1 for c in self.cells.values() if c.state == CellState.ACTIVE),
                    'dormant_cells': sum(1 for c in self.cells.values() if c.state == CellState.DORMANT),
                    'hibernate_cells': sum(1 for c in self.cells.values() if c.state == CellState.HIBERNATE),
                    'last_saved': datetime.now().isoformat()
                }
            }
            with open(cells_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[NETWORK] Save error: {e}")
    
    def add_cell(self, cell: MemoryCell) -> str:
        """
        添加细胞到网络
        
        Args:
            cell: 记忆细胞
        
        Returns:
            细胞ID
        """
        self.cells[cell.id] = cell
        self._save_network()
        return cell.id
    
    def get_cell(self, cell_id: str) -> Optional[MemoryCell]:
        """获取细胞"""
        return self.cells.get(cell_id)
    
    def remove_cell(self, cell_id: str) -> bool:
        """
        移除细胞（仅用于测试，实际永不删除）
        
        注意：在实际系统中，细胞永不删除，只是进入深度休眠
        """
        if cell_id in self.cells:
            cell = self.cells[cell_id]
            # 让细胞进入深度休眠
            cell.energy = 0.01
            cell.state = CellState.HIBERNATE
            self._save_network()
            return True
        return False
    
    def connect_cells(self, source_id: str, target_id: str,
                      synapse_type: SynapseType = SynapseType.ASSOCIATIVE,
                      strength: float = 1.0, weight: float = 1.0,
                      bidirectional: bool = True) -> bool:
        """
        建立细胞间突触连接
        
        Args:
            source_id: 源细胞ID
            target_id: 目标细胞ID
            synapse_type: 突触类型
            strength: 连接强度
            weight: 权重
            bidirectional: 是否双向
        
        Returns:
            是否成功
        """
        source = self.cells.get(source_id)
        target = self.cells.get(target_id)
        
        if not source or not target:
            return False
        
        # 检查突触数量限制
        if len(source.synapses) >= self.MAX_SYNAPSES_PER_CELL:
            return False
        
        # 建立连接
        synapse = source.connect(target_id, synapse_type, strength, weight, bidirectional)
        
        # 更新反向索引
        self.synapse_index[target_id].add(source_id)
        
        # 双向连接
        if bidirectional and len(target.synapses) < self.MAX_SYNAPSES_PER_CELL:
            target.connect(source_id, synapse_type, strength, weight, bidirectional=False)
            self.synapse_index[source_id].add(target_id)
        
        self._save_network()
        return True
    
    def pulse(self, source_id: str, pulse_type: PulseType = PulseType.ACTIVATION,
              strength: float = 1.0, visited: Set[str] = None) -> List[NeuralPulse]:
        """
        发送神经脉冲并传导
        
        Args:
            source_id: 脉冲源
            pulse_type: 脉冲类型
            strength: 脉冲强度
            visited: 已访问节点（用于递归）
        
        Returns:
            激活的脉冲列表
        """
        if visited is None:
            visited = set()
        
        pulses = []
        source = self.cells.get(source_id)
        
        if not source or source_id in visited:
            return pulses
        
        if strength < self.MIN_PULSE_STRENGTH:
            return pulses
        
        visited.add(source_id)
        
        # 激活源细胞
        if pulse_type == PulseType.ACTIVATION:
            source.activate(strength)
        elif pulse_type == PulseType.QUERY:
            source.receive_pulse(strength)
        
        # 创建脉冲记录
        pulse = NeuralPulse(
            source_id=source_id,
            target_id=source_id,
            pulse_type=pulse_type,
            strength=strength,
            depth=0,
            path=[source_id]
        )
        pulses.append(pulse)
        
        # 向突触连接的细胞传导
        for synapse in source.synapses:
            target_id = synapse.target_id
            
            if target_id in visited:
                continue
            
            # 计算传导强度
            transmitted_strength = strength * synapse.weight * self.PULSE_DECAY_RATE
            
            # 递归传导
            sub_pulses = self.pulse(
                target_id, pulse_type, transmitted_strength, visited.copy()
            )
            
            for sp in sub_pulses:
                sp.depth += 1
                sp.path = [source_id] + sp.path
            
            pulses.extend(sub_pulses)
            
            # 强化突触
            synapse.pulse_count += 1
            synapse.strength = min(1.0, synapse.strength + 0.05)
        
        self._save_network()
        return pulses
    
    def auto_connect(self, cell_id: str, similarity_threshold: float = 0.7) -> List[str]:
        """
        自动发现并建立连接
        
        基于内容相似度自动建立突触连接
        
        Args:
            cell_id: 细胞ID
            similarity_threshold: 相似度阈值
        
        Returns:
            新建立的连接ID列表
        """
        cell = self.cells.get(cell_id)
        if not cell:
            return []
        
        new_connections = []
        
        # 提取关键词
        cell_keywords = set(cell.keywords)
        
        # 遍历其他细胞，寻找相似节点
        for other_id, other_cell in self.cells.items():
            if other_id == cell_id:
                continue
            
            # 计算关键词重叠
            other_keywords = set(other_cell.keywords)
            overlap = len(cell_keywords & other_keywords)
            union = len(cell_keywords | other_keywords)
            
            if union == 0:
                continue
            
            similarity = overlap / union
            
            # 超过阈值则建立连接
            if similarity >= similarity_threshold:
                # 确定突触类型
                synapse_type = self._determine_synapse_type(cell, other_cell)
                
                # 建立连接
                if self.connect_cells(cell_id, other_id, synapse_type, strength=similarity):
                    new_connections.append(other_id)
        
        return new_connections
    
    def _determine_synapse_type(self, cell1: MemoryCell, cell2: MemoryCell) -> SynapseType:
        """根据两个细胞的特征确定突触类型"""
        # 同类型 -> 语义型
        if cell1.gene == cell2.gene:
            return SynapseType.SEMANTIC
        
        # 基因类型映射
        type_pairs = {
            (CellGene.PROJECT, CellGene.USER): SynapseType.ASSOCIATIVE,
            (CellGene.USER, CellGene.PROJECT): SynapseType.ASSOCIATIVE,
            (CellGene.FEEDBACK, CellGene.PROJECT): SynapseType.CAUSAL,
            (CellGene.PROJECT, CellGene.FEEDBACK): SynapseType.CAUSAL,
            (CellGene.INSIGHT, CellGene.PROJECT): SynapseType.HIERARCHICAL,
            (CellGene.PATTERN, CellGene.USER): SynapseType.SEMANTIC,
        }
        
        key = (cell1.gene, cell2.gene)
        return type_pairs.get(key, SynapseType.ASSOCIATIVE)
    
    def get_active_cells(self) -> List[MemoryCell]:
        """获取所有活跃细胞"""
        return [c for c in self.cells.values() if c.state == CellState.ACTIVE]
    
    def get_dormant_cells(self) -> List[MemoryCell]:
        """获取所有休眠细胞"""
        return [c for c in self.cells.values() if c.state == CellState.DORMANT]
    
    def get_hibernate_cells(self) -> List[MemoryCell]:
        """获取所有深度休眠细胞"""
        return [c for c in self.cells.values() if c.state == CellState.HIBERNATE]
    
    def wake_cell(self, cell_id: str) -> bool:
        """
        唤醒休眠细胞
        
        Args:
            cell_id: 细胞ID
        
        Returns:
            是否成功唤醒
        """
        cell = self.cells.get(cell_id)
        if not cell:
            return False
        
        # 注入能量
        cell.energy = 0.6
        cell.state = CellState.ACTIVE
        cell.last_active = datetime.now().isoformat()
        
        self._save_network()
        return True
    
    def decay_all(self, days: float = 1.0):
        """
        全网能量衰减
        
        Args:
            days: 衰减天数
        """
        for cell in self.cells.values():
            cell.decay(days)
        
        self._save_network()
    
    def get_network_stats(self) -> Dict:
        """获取网络统计信息"""
        total_synapses = sum(len(c.synapses) for c in self.cells.values())
        
        return {
            'total_cells': len(self.cells),
            'active_cells': len(self.get_active_cells()),
            'dormant_cells': len(self.get_dormant_cells()),
            'hibernate_cells': len(self.get_hibernate_cells()),
            'total_synapses': total_synapses,
            'avg_synapses_per_cell': total_synapses / len(self.cells) if self.cells else 0,
            'avg_energy': sum(c.energy for c in self.cells.values()) / len(self.cells) if self.cells else 0
        }
    
    def visualize_network(self, max_depth: int = 2) -> str:
        """
        可视化网络结构
        
        Returns:
            ASCII艺术形式的网络图
        """
        lines = []
        lines.append("=" * 60)
        lines.append("            NEURAL MEMORY NETWORK VISUALIZATION")
        lines.append("=" * 60)
        
        active = self.get_active_cells()
        dormant = self.get_dormant_cells()
        hibernate = self.get_hibernate_cells()
        
        # 活跃细胞
        lines.append(f"\n[ACTIVE CELLS: {len(active)}]")
        for cell in active[:10]:  # 最多显示10个
            connections = len(cell.synapses)
            lines.append(f"  ● {cell.id[:20]}... (E:{cell.energy:.2f}, C:{connections})")
        
        if len(active) > 10:
            lines.append(f"  ... and {len(active) - 10} more")
        
        # 休眠细胞
        lines.append(f"\n[DORMANT CELLS: {len(dormant)}]")
        for cell in dormant[:5]:
            lines.append(f"  ○ {cell.id[:20]}... (E:{cell.energy:.2f})")
        
        if len(dormant) > 5:
            lines.append(f"  ... and {len(dormant) - 5} more")
        
        # 深度休眠细胞
        lines.append(f"\n[HIBERNATE CELLS: {len(hibernate)}]")
        lines.append(f"  • {len(hibernate)} cells in deep sleep (永不删除)")
        
        lines.append("\n" + "=" * 60)
        lines.append("● = Active    ○ = Dormant    • = Hibernate")
        lines.append("E = Energy    C = Connections")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def find_path(self, source_id: str, target_id: str) -> List[str]:
        """
        查找两个细胞间的最短路径
        
        Args:
            source_id: 起点细胞ID
            target_id: 终点细胞ID
        
        Returns:
            路径上的细胞ID列表，如果不存在路径返回空列表
        """
        if source_id not in self.cells or target_id not in self.cells:
            return []
        
        if source_id == target_id:
            return [source_id]
        
        # BFS查找
        visited = {source_id}
        queue = deque([(source_id, [source_id])])
        
        while queue:
            current, path = queue.popleft()
            
            cell = self.cells.get(current)
            if not cell:
                continue
            
            for synapse in cell.synapses:
                neighbor = synapse.target_id
                
                if neighbor == target_id:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return []  # 未找到路径
    
    def get_neighborhood(self, cell_id: str, depth: int = 2) -> Dict:
        """
        获取细胞的邻域
        
        Args:
            cell_id: 细胞ID
            depth: 邻域深度
        
        Returns:
            邻域信息
        """
        cell = self.cells.get(cell_id)
        if not cell:
            return {}
        
        neighborhood = {
            'center': cell_id,
            'depth_1': [],
            'depth_2': [],
            'depth_3': []
        }
        
        visited = {cell_id}
        
        # Depth 1
        for synapse in cell.synapses:
            target_id = synapse.target_id
            if target_id in self.cells:
                neighborhood['depth_1'].append({
                    'id': target_id,
                    'type': synapse.synapse_type.value,
                    'strength': synapse.strength
                })
                visited.add(target_id)
        
        # Depth 2 & 3
        if depth >= 2:
            for n1 in neighborhood['depth_1']:
                n1_cell = self.cells.get(n1['id'])
                if n1_cell:
                    for synapse in n1_cell.synapses:
                        target_id = synapse.target_id
                        if target_id not in visited and target_id in self.cells:
                            neighborhood['depth_2'].append({
                                'id': target_id,
                                'via': n1['id'],
                                'type': synapse.synapse_type.value
                            })
                            visited.add(target_id)
        
        return neighborhood


def main():
    parser = argparse.ArgumentParser(description="Memory Neural Network - 记忆神经网络")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # create命令 - 创建网络
    create_parser = subparsers.add_parser("create", help="创建新细胞并加入网络")
    create_parser.add_argument("--content", required=True, help="记忆内容")
    create_parser.add_argument("--type", default="user", help="细胞类型")
    
    # connect命令
    connect_parser = subparsers.add_parser("connect", help="建立突触连接")
    connect_parser.add_argument("--from", dest="source", required=True, help="源细胞ID")
    connect_parser.add_argument("--to", dest="target", required=True, help="目标细胞ID")
    connect_parser.add_argument("--type", default="associative", help="突触类型")
    
    # pulse命令
    pulse_parser = subparsers.add_parser("pulse", help="发送神经脉冲")
    pulse_parser.add_argument("--source", required=True, help="脉冲源细胞ID")
    pulse_parser.add_argument("--strength", type=float, default=1.0, help="脉冲强度")
    
    # stats命令
    stats_parser = subparsers.add_parser("stats", help="显示网络统计")
    
    # visualize命令
    vis_parser = subparsers.add_parser("visualize", help="可视化网络")
    
    # auto-connect命令
    auto_parser = subparsers.add_parser("auto-connect", help="自动建立连接")
    auto_parser.add_argument("--cell", required=True, help="细胞ID")
    auto_parser.add_argument("--threshold", type=float, default=0.7, help="相似度阈值")
    
    args = parser.parse_args()
    
    network = MemoryNeuralNetwork()
    
    if args.command == "create":
        gene_map = {
            "user": CellGene.USER,
            "feedback": CellGene.FEEDBACK,
            "project": CellGene.PROJECT,
            "reference": CellGene.REFERENCE
        }
        gene = gene_map.get(args.type, CellGene.USER)
        cell = create_cell(args.content, gene)
        network.add_cell(cell)
        print(f"[CREATE] Created cell: {cell.id}")
        print(json.dumps(cell.to_dict(), ensure_ascii=False, indent=2))
    
    elif args.command == "connect":
        synapse_type = SynapseType(args.type)
        if network.connect_cells(args.source, args.target, synapse_type):
            print(f"[CONNECT] Connected {args.source} -> {args.target}")
        else:
            print(f"[ERROR] Failed to connect")
    
    elif args.command == "pulse":
        pulses = network.pulse(args.source, PulseType.ACTIVATION, args.strength)
        print(f"[PULSE] Activated {len(pulses)} cells")
        for p in pulses:
            print(f"  {p.target_id} (strength: {p.strength:.3f}, depth: {p.depth})")
    
    elif args.command == "stats":
        stats = network.get_network_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    elif args.command == "visualize":
        print(network.visualize_network())
    
    elif args.command == "auto-connect":
        new_connections = network.auto_connect(args.cell, args.threshold)
        print(f"[AUTO-CONNECT] Created {len(new_connections)} connections")
        for conn_id in new_connections:
            print(f"  -> {conn_id}")


if __name__ == "__main__":
    from enum import Enum
    main()
