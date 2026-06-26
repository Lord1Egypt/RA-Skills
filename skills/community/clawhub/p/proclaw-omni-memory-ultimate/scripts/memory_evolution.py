#!/usr/bin/env python3
"""
Memory Evolution - 记忆演化机制
实现记忆的动态性：可更新、可修正、可整合、可重构
基于认知科学的 Bartlett 记忆重构理论
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

from memory_cell import MemoryCell, CellState, CellGene, Synapse, SynapseType
from neural_network import MemoryNeuralNetwork
from semantic_memory import SemanticMemoryEngine


class EvolutionType(Enum):
    """演化类型"""
    ENHANCE = "enhance"         # 增强：新信息强化原有记忆
    CORRECT = "correct"         # 修正：纠正错误记忆
    MERGE = "merge"             # 整合：合并相似记忆
    ABSTRACT = "abstract"       # 抽象：提炼共性生成抽象记忆
    DECAY = "decay"             # 衰减：自然遗忘
    RECONSTRUCT = "reconstruct" # 重构：基于回忆修改记忆


class ConflictResolution(Enum):
    """冲突解决策略"""
    KEEP_OLD = "keep_old"       # 保留旧记忆
    KEEP_NEW = "keep_new"       # 采用新信息
    MERGE = "merge"             # 合并两者
    CREATE_NEW = "create_new"   # 创建新记忆保留差异


@dataclass
class EvolutionEvent:
    """演化事件记录"""
    cell_id: str
    evolution_type: EvolutionType
    before: Dict               # 演化前状态
    after: Dict                # 演化后状态
    trigger: str               # 触发原因
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'cell_id': self.cell_id,
            'type': self.evolution_type.value,
            'before': self.before,
            'after': self.after,
            'trigger': self.trigger,
            'timestamp': self.timestamp
        }


class MemoryEvolutionEngine:
    """
    记忆演化引擎 - 让记忆"活"起来
    
    核心理念（Bartlett 记忆重构理论）：
    - 记忆不是"回放"而是"重构"
    - 每次回忆都会修改记忆
    - 记忆是动态的、可演化的
    
    演化类型：
    1. 增强（Enhance）：新信息强化原有记忆
    2. 修正（Correct）：纠正错误记忆
    3. 整合（Merge）：合并相似记忆
    4. 抽象（Abstract）：提炼共性生成抽象记忆
    5. 衰减（Decay）：自然遗忘
    6. 重构（Reconstruct）：基于回忆修改记忆
    """
    
    # 演化阈值
    SIMILARITY_MERGE_THRESHOLD = 0.85    # 合并阈值
    SIMILARITY_DUPLICATE_THRESHOLD = 0.95 # 重复阈值
    CORRECTION_CONFIDENCE_THRESHOLD = 0.8 # 修正置信度
    
    # 演化参数
    MAX_EVOLUTION_HISTORY = 100           # 最大演化历史
    EVOLUTION_COOLDOWN = 3600             # 演化冷却期（秒）
    
    def __init__(self, network: MemoryNeuralNetwork = None,
                 semantic_engine: SemanticMemoryEngine = None):
        """
        初始化演化引擎
        
        Args:
            network: 神经网络
            semantic_engine: 语义引擎
        """
        self.network = network
        self.semantic_engine = semantic_engine
        
        # 演化历史
        self.evolution_history: List[EvolutionEvent] = []
        
        # 演化统计
        self.stats = {
            'enhancements': 0,
            'corrections': 0,
            'merges': 0,
            'abstractions': 0,
            'reconstructions': 0
        }
        
        # 最近演化时间
        self._last_evolution: Dict[str, str] = {}
    
    def evolve(self, cell: MemoryCell, new_info: Dict,
               strategy: ConflictResolution = ConflictResolution.MERGE) -> EvolutionEvent:
        """
        核心演化方法 - 让记忆进化
        
        Args:
            cell: 目标细胞
            new_info: 新信息 {'content': str, 'importance': float, ...}
            strategy: 冲突解决策略
        
        Returns:
            演化事件
        """
        # 检查冷却期
        if not self._can_evolve(cell.id):
            return None
        
        # 记录演化前状态
        before = cell.to_dict()
        
        # 判断演化类型
        evolution_type = self._determine_evolution_type(cell, new_info)
        
        # 执行演化
        if evolution_type == EvolutionType.ENHANCE:
            self._enhance(cell, new_info)
        elif evolution_type == EvolutionType.CORRECT:
            self._correct(cell, new_info)
        elif evolution_type == EvolutionType.MERGE:
            self._merge_info(cell, new_info)
        elif evolution_type == EvolutionType.ABSTRACT:
            self._abstract(cell, new_info)
        
        # 记录演化后状态
        after = cell.to_dict()
        
        # 创建演化事件
        event = EvolutionEvent(
            cell_id=cell.id,
            evolution_type=evolution_type,
            before=before,
            after=after,
            trigger=new_info.get('trigger', 'unknown')
        )
        
        # 记录历史
        self._record_evolution(event)
        
        return event
    
    def _determine_evolution_type(self, cell: MemoryCell, new_info: Dict) -> EvolutionType:
        """判断演化类型"""
        new_content = new_info.get('content', '')
        
        # 计算相似度
        if self.semantic_engine:
            cell_vector = self.semantic_engine.embed(cell.content)
            new_vector = self.semantic_engine.embed(new_content)
            similarity = self.semantic_engine.cosine_similarity(cell_vector, new_vector)
        else:
            # 简单相似度
            cell_words = set(cell.content.lower().split())
            new_words = set(new_content.lower().split())
            overlap = len(cell_words & new_words)
            union = len(cell_words | new_words)
            similarity = overlap / union if union > 0 else 0
        
        # 判断类型
        if similarity >= self.SIMILARITY_DUPLICATE_THRESHOLD:
            return EvolutionType.ENHANCE  # 高度相似 = 增强
        elif similarity >= self.SIMILARITY_MERGE_THRESHOLD:
            return EvolutionType.MERGE    # 较高相似 = 整合
        elif new_info.get('is_correction', False):
            return EvolutionType.CORRECT  # 明确标记为修正
        elif new_info.get('is_abstract', False):
            return EvolutionType.ABSTRACT # 明确标记为抽象
        else:
            return EvolutionType.ENHANCE  # 默认增强
    
    def _enhance(self, cell: MemoryCell, new_info: Dict):
        """
        增强记忆
        
        当新信息与原记忆高度一致时：
        - 增加能量
        - 提升重要性
        - 增加访问计数
        """
        # 能量提升
        cell.energy = min(1.0, cell.energy + 0.1)
        
        # 重要性提升
        if 'importance' in new_info:
            cell.importance = (cell.importance + new_info['importance']) / 2
        
        # 更新最后活跃时间
        cell.last_active = datetime.now().isoformat()
        
        # 更新可信度
        cell.trust_score = min(1.0, cell.trust_score + 0.05)
        
        # 统计
        self.stats['enhancements'] += 1
        
        print(f"[EVOLUTION] Enhanced cell {cell.id[:12]}: energy={cell.energy:.2f}")
    
    def _correct(self, cell: MemoryCell, new_info: Dict):
        """
        修正记忆
        
        当发现记忆有误时：
        - 更新内容
        - 降低可信度
        - 记录修正历史
        """
        old_content = cell.content
        
        # 更新内容
        if 'content' in new_info:
            cell.content = new_info['content']
            cell.keywords = cell._extract_keywords(new_info['content'])
        
        # 更新其他属性
        if 'importance' in new_info:
            cell.importance = new_info['importance']
        
        # 降低可信度（因为之前是错的）
        cell.trust_score = max(0.3, cell.trust_score - 0.1)
        
        # 统计
        self.stats['corrections'] += 1
        
        print(f"[EVOLUTION] Corrected cell {cell.id[:12]}")
    
    def _merge_info(self, cell: MemoryCell, new_info: Dict):
        """
        整合信息
        
        当新信息与原记忆部分重叠时：
        - 合并内容
        - 综合属性
        - 建立关联
        """
        old_content = cell.content
        new_content = new_info.get('content', '')
        
        # 智能合并内容
        merged_content = self._smart_merge(old_content, new_content)
        cell.content = merged_content
        cell.keywords = cell._extract_keywords(merged_content)
        
        # 综合属性
        if 'importance' in new_info:
            cell.importance = max(cell.importance, new_info['importance'])
        
        # 能量提升
        cell.energy = min(1.0, cell.energy + 0.05)
        
        # 统计
        self.stats['merges'] += 1
        
        print(f"[EVOLUTION] Merged cell {cell.id[:12]}")
    
    def _smart_merge(self, old: str, new: str) -> str:
        """智能合并两段文本"""
        # 简单策略：如果新内容更长且包含旧内容，用新的
        if new in old:
            return old
        elif old in new:
            return new
        else:
            # 合并不重叠的信息
            old_set = set(old.split())
            new_set = set(new.split())
            
            # 如果重叠度高，选择更完整的
            overlap = len(old_set & new_set)
            if overlap > len(old_set) * 0.5:
                return new if len(new) > len(old) else old
            else:
                # 合并
                return f"{old} | {new}"
    
    def _abstract(self, cell: MemoryCell, new_info: Dict):
        """
        抽象化
        
        从多个记忆中提炼共性，生成抽象记忆
        """
        # 标记为抽象类型
        cell.gene = CellGene.PATTERN
        
        # 统计
        self.stats['abstractions'] += 1
        
        print(f"[EVOLUTION] Abstracted cell {cell.id[:12]}")
    
    def reconstruct_on_recall(self, cell: MemoryCell, context: str) -> EvolutionEvent:
        """
        回忆时重构记忆
        
        基于 Bartlett 理论：每次回忆都会修改记忆
        
        Args:
            cell: 被回忆的细胞
            context: 回忆时的上下文
        
        Returns:
            演化事件
        """
        # 记录演化前状态
        before = {
            'energy': cell.energy,
            'access_count': cell.access_count
        }
        
        # 重构：增加能量和访问计数
        cell.activate(1.0)
        
        # 根据上下文微调（简化版）
        # 实际系统可以更复杂地分析上下文并调整记忆
        
        # 记录演化后状态
        after = {
            'energy': cell.energy,
            'access_count': cell.access_count
        }
        
        # 创建演化事件
        event = EvolutionEvent(
            cell_id=cell.id,
            evolution_type=EvolutionType.RECONSTRUCT,
            before=before,
            after=after,
            trigger=f"recall: {context[:50]}"
        )
        
        self._record_evolution(event)
        self.stats['reconstructions'] += 1
        
        return event
    
    def find_duplicate_memories(self, cells: List[MemoryCell]) -> List[List[str]]:
        """
        发现重复记忆
        
        Returns:
            [[duplicate_group], ...]
        """
        if not self.semantic_engine:
            return []
        
        duplicates = []
        processed = set()
        
        for i, cell1 in enumerate(cells):
            if cell1.id in processed:
                continue
            
            group = [cell1.id]
            processed.add(cell1.id)
            
            for j, cell2 in enumerate(cells[i+1:], i+1):
                if cell2.id in processed:
                    continue
                
                # 计算相似度
                v1 = self.semantic_engine.embed(cell1.content)
                v2 = self.semantic_engine.embed(cell2.content)
                sim = self.semantic_engine.cosine_similarity(v1, v2)
                
                if sim >= self.SIMILARITY_DUPLICATE_THRESHOLD:
                    group.append(cell2.id)
                    processed.add(cell2.id)
            
            if len(group) > 1:
                duplicates.append(group)
        
        return duplicates
    
    def merge_duplicates(self, cells: List[MemoryCell]) -> int:
        """
        合并重复记忆
        
        Returns:
            合并数量
        """
        duplicates = self.find_duplicate_memories(cells)
        merged_count = 0
        
        for group in duplicates:
            # 选择能量最高的作为主记忆
            main_cell = max(
                [c for c in cells if c.id in group],
                key=lambda c: c.energy
            )
            
            # 将其他记忆的能量转移给主记忆
            for cell_id in group:
                if cell_id == main_cell.id:
                    continue
                
                cell = next((c for c in cells if c.id == cell_id), None)
                if cell:
                    # 转移能量
                    main_cell.energy = min(1.0, main_cell.energy + cell.energy * 0.3)
                    
                    # 建立连接
                    main_cell.connect(cell_id, SynapseType.ASSOCIATIVE, strength=0.5)
                    
                    # 将重复记忆设为深度休眠
                    cell.state = CellState.HIBERNATE
                    cell.energy = 0.01
                    
                    merged_count += 1
        
        return merged_count
    
    def decay_memories(self, cells: List[MemoryCell], days: float = 1.0):
        """
        自然衰减
        
        使用艾宾浩斯遗忘曲线
        """
        for cell in cells:
            # 艾宾浩斯公式：R = e^(-t/S)
            # R = 保持率, t = 时间, S = 记忆强度
            import math
            
            # 使用重要性作为记忆强度
            strength = cell.importance * 10  # 放大以减缓衰减
            
            # 计算保持率
            retention = math.exp(-days / strength)
            
            # 应用衰减
            decay_amount = (1 - retention) * 0.1
            cell.energy = max(0.01, cell.energy - decay_amount)
            
            # 更新状态
            if cell.energy <= 0.1:
                cell.state = CellState.HIBERNATE
            elif cell.energy <= 0.5:
                cell.state = CellState.DORMANT
    
    def _can_evolve(self, cell_id: str) -> bool:
        """检查是否可以演化（冷却期检查）"""
        if cell_id not in self._last_evolution:
            return True
        
        last_time = datetime.fromisoformat(self._last_evolution[cell_id])
        elapsed = (datetime.now() - last_time).total_seconds()
        
        return elapsed >= self.EVOLUTION_COOLDOWN
    
    def _record_evolution(self, event: EvolutionEvent):
        """记录演化事件"""
        self.evolution_history.append(event)
        self._last_evolution[event.cell_id] = event.timestamp
        
        # 限制历史大小
        if len(self.evolution_history) > self.MAX_EVOLUTION_HISTORY:
            self.evolution_history = self.evolution_history[-self.MAX_EVOLUTION_HISTORY:]
    
    def get_evolution_stats(self) -> Dict:
        """获取演化统计"""
        return {
            **self.stats,
            'total_evolutions': sum(self.stats.values()),
            'recent_evolutions': len(self.evolution_history)
        }
    
    def get_evolution_history(self, cell_id: str = None, limit: int = 20) -> List[Dict]:
        """获取演化历史"""
        history = self.evolution_history
        
        if cell_id:
            history = [e for e in history if e.cell_id == cell_id]
        
        return [e.to_dict() for e in history[-limit:]]


def main():
    parser = argparse.ArgumentParser(description="Memory Evolution Engine - 记忆演化引擎")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # enhance命令
    enhance_parser = subparsers.add_parser("enhance", help="增强记忆")
    enhance_parser.add_argument("--id", required=True, help="细胞ID")
    enhance_parser.add_argument("--info", required=True, help="新信息")
    
    # correct命令
    correct_parser = subparsers.add_parser("correct", help="修正记忆")
    correct_parser.add_argument("--id", required=True, help="细胞ID")
    correct_parser.add_argument("--content", required=True, help="正确内容")
    
    # merge命令
    merge_parser = subparsers.add_parser("merge", help="整合记忆")
    merge_parser.add_argument("--ids", required=True, help="细胞ID列表(逗号分隔)")
    
    # stats命令
    subparsers.add_parser("stats", help="演化统计")
    
    # history命令
    history_parser = subparsers.add_parser("history", help="演化历史")
    history_parser.add_argument("--id", help="细胞ID")
    history_parser.add_argument("--limit", type=int, default=20, help="数量限制")
    
    args = parser.parse_args()
    
    engine = MemoryEvolutionEngine()
    
    if args.command == "enhance":
        print(f"[ENHANCE] Would enhance cell {args.id} with: {args.info}")
    
    elif args.command == "correct":
        print(f"[CORRECT] Would correct cell {args.id} to: {args.content}")
    
    elif args.command == "merge":
        ids = args.ids.split(',')
        print(f"[MERGE] Would merge cells: {ids}")
    
    elif args.command == "stats":
        stats = engine.get_evolution_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    elif args.command == "history":
        history = engine.get_evolution_history(args.id, args.limit)
        print(json.dumps(history, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
