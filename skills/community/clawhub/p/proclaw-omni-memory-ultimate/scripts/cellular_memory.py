#!/usr/bin/env python3
"""
Cellular Memory System - 细胞式记忆系统
整合所有组件，提供统一的细胞式记忆管理接口
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

# 导入核心组件
from memory_cell import MemoryCell, CellState, CellGene, Synapse, SynapseType, create_cell
from neural_network import MemoryNeuralNetwork, PulseType
from cell_lifecycle import CellLifecycleManager, DivisionTrigger


class CellularMemorySystem:
    """
    细胞式记忆系统 - 有生命力的智能记忆
    
    核心理念：
    1. 细胞式结构 - 每个记忆是一个有生命力的细胞
    2. 蜘蛛网网络 - 多节点多链接交叉关联
    3. 永恒存在 - 记忆永不删除，只是沉默
    4. 自主进化 - 细胞可分裂、生发、进化
    
    系统架构：
    - 记忆细胞：有生命力的记忆单元
    - 神经网络：蜘蛛网式关联网络
    - 生命周期：诞生、生长、分裂、休眠、唤醒
    - 永恒存储：结构持久化，永不丢失
    """
    
    def __init__(self, storage_path: str = "./cellular_memory"):
        """
        初始化细胞式记忆系统
        
        Args:
            storage_path: 存储路径
        """
        self.storage_path = storage_path
        
        # 确保存储目录存在
        os.makedirs(storage_path, exist_ok=True)
        
        # 初始化核心组件
        self.network = MemoryNeuralNetwork(os.path.join(storage_path, "network"))
        self.lifecycle = CellLifecycleManager(self.network)
        
        # 系统状态
        self.initialized_at = datetime.now().isoformat()
        
        print(f"[CELLULAR MEMORY] Initialized at {storage_path}")
    
    def remember(self, content: str, gene: str = "user",
                 importance: float = 0.7, auto_connect: bool = True) -> Dict:
        """
        记忆 - 创建新的记忆细胞
        
        Args:
            content: 记忆内容
            gene: 细胞类型 (user/feedback/project/reference)
            importance: 重要性 (0-1)
            auto_connect: 是否自动建立关联
        
        Returns:
            创建的细胞信息
        """
        # 转换基因类型
        gene_map = {
            "user": CellGene.USER,
            "feedback": CellGene.FEEDBACK,
            "project": CellGene.PROJECT,
            "reference": CellGene.REFERENCE
        }
        cell_gene = gene_map.get(gene, CellGene.USER)
        
        # 创建细胞
        cell = self.lifecycle.birth(content, cell_gene, importance)
        
        # 自动建立关联
        if auto_connect:
            new_connections = self.network.auto_connect(cell.id)
            print(f"[REMEMBER] Auto-connected to {len(new_connections)} cells")
        
        return {
            'success': True,
            'cell_id': cell.id,
            'state': cell.state.value,
            'energy': cell.energy,
            'connections': len(cell.synapses)
        }
    
    def recall(self, query: str, top_k: int = 5,
               activate: bool = True) -> List[Dict]:
        """
        回忆 - 激活并检索相关记忆
        
        Args:
            query: 查询内容
            top_k: 返回数量
            activate: 是否激活细胞
        
        Returns:
            相关记忆列表
        """
        # 查找相关细胞（基于关键词匹配）
        results = []
        query_keywords = set(query.lower().split())
        
        # 按活跃度和相关度排序
        scored_cells = []
        for cell in self.network.cells.values():
            if cell.state == CellState.HIBERNATE:
                # 深度休眠细胞降低优先级
                score = 0.1
            else:
                # 计算相关度
                cell_keywords = set(k.lower() for k in cell.keywords)
                overlap = len(query_keywords & cell_keywords)
                score = overlap * cell.energy * cell.importance
            
            if score > 0:
                scored_cells.append((cell, score))
        
        # 排序并取top_k
        scored_cells.sort(key=lambda x: x[1], reverse=True)
        top_cells = scored_cells[:top_k]
        
        for cell, score in top_cells:
            # 激活细胞
            if activate:
                cell.activate(1.0)
                # 发送脉冲激活相关细胞
                self.network.pulse(cell.id, PulseType.ACTIVATION, 0.5)
            
            results.append({
                'cell_id': cell.id,
                'content': cell.content,
                'gene': cell.gene.value,
                'energy': cell.energy,
                'state': cell.state.value,
                'importance': cell.importance,
                'relevance_score': score,
                'connections': len(cell.synapses),
                'age': cell.age
            })
        
        self.network._save_network()
        return results
    
    def connect(self, source_id: str, target_id: str,
                connection_type: str = "associative") -> Dict:
        """
        连接 - 建立突触连接
        
        Args:
            source_id: 源细胞ID
            target_id: 目标细胞ID
            connection_type: 连接类型
        
        Returns:
            连接结果
        """
        type_map = {
            "associative": SynapseType.ASSOCIATIVE,
            "causal": SynapseType.CAUSAL,
            "temporal": SynapseType.TEMPORAL,
            "hierarchical": SynapseType.HIERARCHICAL,
            "semantic": SynapseType.SEMANTIC
        }
        synapse_type = type_map.get(connection_type, SynapseType.ASSOCIATIVE)
        
        success = self.network.connect_cells(source_id, target_id, synapse_type)
        
        return {
            'success': success,
            'source_id': source_id,
            'target_id': target_id,
            'connection_type': connection_type
        }
    
    def evolve(self, cell_id: str = None) -> Dict:
        """
        进化 - 触发细胞分裂或网络生长
        
        Args:
            cell_id: 指定细胞ID，为None则全网进化
        
        Returns:
            进化结果
        """
        results = {
            'divisions': [],
            'new_connections': []
        }
        
        if cell_id:
            # 单细胞进化
            result = self.lifecycle.auto_divide(cell_id)
            if result:
                results['divisions'].append({
                    'parent_id': result.parent_id,
                    'child_id': result.child_id,
                    'trigger': result.trigger.value
                })
        else:
            # 全网进化
            for cid in list(self.network.cells.keys()):
                # 尝试分裂
                result = self.lifecycle.auto_divide(cid)
                if result:
                    results['divisions'].append({
                        'parent_id': result.parent_id,
                        'child_id': result.child_id,
                        'trigger': result.trigger.value
                    })
                
                # 自动建立连接
                new_conns = self.network.auto_connect(cid)
                results['new_connections'].extend([
                    {'source': cid, 'target': tid} for tid in new_conns
                ])
        
        return results
    
    def activate(self, cell_id: str, strength: float = 1.0) -> Dict:
        """
        激活 - 激活细胞及其网络
        
        Args:
            cell_id: 细胞ID
            strength: 激活强度
        
        Returns:
            激活结果
        """
        cell = self.network.get_cell(cell_id)
        if not cell:
            return {'success': False, 'error': 'Cell not found'}
        
        # 唤醒（如果在休眠）
        if cell.state == CellState.HIBERNATE:
            self.lifecycle.wake(cell_id)
        
        # 激活
        boost = cell.activate(strength)
        
        # 发送脉冲
        pulses = self.network.pulse(cell_id, PulseType.ACTIVATION, strength)
        
        return {
            'success': True,
            'cell_id': cell_id,
            'energy_boost': boost,
            'new_energy': cell.energy,
            'activated_count': len(pulses)
        }
    
    def silence(self, cell_id: str) -> Dict:
        """
        沉默 - 让细胞进入休眠
        
        注意：永不删除，只是沉默
        
        Args:
            cell_id: 细胞ID
        
        Returns:
            操作结果
        """
        cell = self.network.get_cell(cell_id)
        if not cell:
            return {'success': False, 'error': 'Cell not found'}
        
        # 进入深度休眠
        self.lifecycle.hibernate(cell_id)
        
        return {
            'success': True,
            'cell_id': cell_id,
            'message': 'Cell is now in deep sleep (never deleted)'
        }
    
    def get_lineage(self, cell_id: str) -> Dict:
        """
        获取谱系 - 查看细胞的家族树
        
        Args:
            cell_id: 细胞ID
        
        Returns:
            家族树信息
        """
        return self.lifecycle.get_family_tree(cell_id)
    
    def get_neighborhood(self, cell_id: str, depth: int = 2) -> Dict:
        """
        获取邻域 - 查看细胞的关联网络
        
        Args:
            cell_id: 细胞ID
            depth: 邻域深度
        
        Returns:
            邻域信息
        """
        return self.network.get_neighborhood(cell_id, depth)
    
    def pulse(self, source_id: str, strength: float = 1.0) -> Dict:
        """
        脉冲 - 发送神经脉冲激活网络
        
        Args:
            source_id: 脉冲源
            strength: 脉冲强度
        
        Returns:
            脉冲传播结果
        """
        pulses = self.network.pulse(source_id, PulseType.ACTIVATION, strength)
        
        return {
            'success': True,
            'source_id': source_id,
            'activated_count': len(pulses),
            'pulse_path': [p.to_dict() for p in pulses[:10]]  # 只返回前10个
        }
    
    def stats(self) -> Dict:
        """
        统计 - 获取系统统计信息
        
        Returns:
            系统统计
        """
        network_stats = self.network.get_network_stats()
        lifecycle_stats = self.lifecycle.get_lifecycle_stats()
        division_stats = self.lifecycle.get_division_stats()
        
        return {
            'network': network_stats,
            'lifecycle': lifecycle_stats,
            'divisions': division_stats,
            'system': {
                'initialized_at': self.initialized_at,
                'storage_path': self.storage_path
            }
        }
    
    def visualize(self) -> str:
        """
        可视化 - 显示网络结构
        
        Returns:
            可视化文本
        """
        return self.network.visualize_network()
    
    def maintain(self) -> Dict:
        """
        维护 - 执行系统维护
        
        Returns:
            维护结果
        """
        # 全网能量衰减
        self.lifecycle.decay_all(1.0)
        
        # 永恒维护
        self.lifecycle.maintain_eternal()
        
        return {
            'success': True,
            'message': 'System maintenance completed',
            'timestamp': datetime.now().isoformat()
        }
    
    def export_state(self) -> Dict:
        """
        导出 - 导出系统状态
        
        Returns:
            系统完整状态
        """
        return {
            'cells': [cell.to_dict() for cell in self.network.cells.values()],
            'lineage': dict(self.lifecycle.lineage),
            'ancestry': self.lifecycle.ancestry,
            'division_history': [vars(d) for d in self.lifecycle.division_history],
            'metadata': {
                'exported_at': datetime.now().isoformat(),
                'total_cells': len(self.network.cells),
                'version': '1.0.0-cellular'
            }
        }
    
    def import_state(self, state: Dict) -> bool:
        """
        导入 - 导入系统状态
        
        Args:
            state: 系统状态
        
        Returns:
            是否成功
        """
        try:
            # 导入细胞
            for cell_data in state.get('cells', []):
                cell = MemoryCell.from_dict(cell_data)
                self.network.cells[cell.id] = cell
            
            # 导入谱系
            for parent_id, children in state.get('lineage', {}).items():
                self.lifecycle.lineage[parent_id] = children
            
            self.lifecycle.ancestry = state.get('ancestry', {})
            
            # 导入分裂历史
            # ... (简化处理)
            
            self.network._save_network()
            return True
        except Exception as e:
            print(f"[IMPORT ERROR] {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Cellular Memory System - 细胞式记忆系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 创建记忆
  python cellular_memory.py remember --content "用户喜欢Python编程" --type user
  
  # 回忆
  python cellular_memory.py recall --query "编程"
  
  # 连接
  python cellular_memory.py connect --from cell_abc --to cell_xyz
  
  # 进化
  python cellular_memory.py evolve --cell cell_abc
  
  # 激活
  python cellular_memory.py activate --id cell_abc
  
  # 统计
  python cellular_memory.py stats
  
  # 可视化
  python cellular_memory.py visualize
        """
    )
    
    parser.add_argument("--storage", default="./cellular_memory", help="存储路径")
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # remember命令
    remember_parser = subparsers.add_parser("remember", help="创建记忆")
    remember_parser.add_argument("--content", required=True, help="记忆内容")
    remember_parser.add_argument("--type", default="user", help="细胞类型")
    remember_parser.add_argument("--importance", type=float, default=0.7, help="重要性")
    remember_parser.add_argument("--no-auto-connect", action="store_true", help="禁用自动连接")
    
    # recall命令
    recall_parser = subparsers.add_parser("recall", help="回忆记忆")
    recall_parser.add_argument("--query", required=True, help="查询内容")
    recall_parser.add_argument("--top-k", type=int, default=5, help="返回数量")
    recall_parser.add_argument("--no-activate", action="store_true", help="不激活细胞")
    
    # connect命令
    connect_parser = subparsers.add_parser("connect", help="建立连接")
    connect_parser.add_argument("--from", dest="source", required=True, help="源细胞ID")
    connect_parser.add_argument("--to", dest="target", required=True, help="目标细胞ID")
    connect_parser.add_argument("--type", default="associative", help="连接类型")
    
    # evolve命令
    evolve_parser = subparsers.add_parser("evolve", help="进化系统")
    evolve_parser.add_argument("--cell", help="指定细胞ID")
    
    # activate命令
    activate_parser = subparsers.add_parser("activate", help="激活细胞")
    activate_parser.add_argument("--id", required=True, help="细胞ID")
    activate_parser.add_argument("--strength", type=float, default=1.0, help="激活强度")
    
    # silence命令
    silence_parser = subparsers.add_parser("silence", help="让细胞沉默")
    silence_parser.add_argument("--id", required=True, help="细胞ID")
    
    # lineage命令
    lineage_parser = subparsers.add_parser("lineage", help="查看谱系")
    lineage_parser.add_argument("--id", required=True, help="细胞ID")
    
    # neighborhood命令
    neighborhood_parser = subparsers.add_parser("neighborhood", help="查看邻域")
    neighborhood_parser.add_argument("--id", required=True, help="细胞ID")
    neighborhood_parser.add_argument("--depth", type=int, default=2, help="邻域深度")
    
    # pulse命令
    pulse_parser = subparsers.add_parser("pulse", help="发送脉冲")
    pulse_parser.add_argument("--source", required=True, help="脉冲源ID")
    pulse_parser.add_argument("--strength", type=float, default=1.0, help="脉冲强度")
    
    # stats命令
    subparsers.add_parser("stats", help="显示统计")
    
    # visualize命令
    subparsers.add_parser("visualize", help="可视化网络")
    
    # maintain命令
    subparsers.add_parser("maintain", help="系统维护")
    
    # export命令
    export_parser = subparsers.add_parser("export", help="导出状态")
    export_parser.add_argument("--output", default="cellular_memory_export.json", help="输出文件")
    
    args = parser.parse_args()
    
    # 初始化系统
    system = CellularMemorySystem(args.storage)
    
    # 执行命令
    if args.command == "remember":
        result = system.remember(
            args.content,
            args.type,
            args.importance,
            not args.no_auto_connect
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "recall":
        results = system.recall(
            args.query,
            args.top_k,
            not args.no_activate
        )
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.command == "connect":
        result = system.connect(args.source, args.target, args.type)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "evolve":
        result = system.evolve(args.cell)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "activate":
        result = system.activate(args.id, args.strength)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "silence":
        result = system.silence(args.id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "lineage":
        result = system.get_lineage(args.id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "neighborhood":
        result = system.get_neighborhood(args.id, args.depth)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "pulse":
        result = system.pulse(args.source, args.strength)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "stats":
        result = system.stats()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "visualize":
        print(system.visualize())
    
    elif args.command == "maintain":
        result = system.maintain()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "export":
        state = system.export_state()
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        print(f"[EXPORT] State exported to {args.output}")


if __name__ == "__main__":
    main()
