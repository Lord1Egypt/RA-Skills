#!/usr/bin/env python3
"""
Proactive Memory - 主动智能系统
预测性记忆推送，工作记忆缓冲，上下文感知
从"被动检索"升级为"主动智能"
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

from memory_cell import MemoryCell, CellState, CellGene
from neural_network import MemoryNeuralNetwork, PulseType
from semantic_memory import SemanticMemoryEngine


class WorkMemorySlot:
    """工作记忆槽位"""
    def __init__(self, cell_id: str, relevance: float, context: str):
        self.cell_id = cell_id
        self.relevance = relevance
        self.context = context
        self.loaded_at = datetime.now().isoformat()
        self.access_count = 0


class IntentType(Enum):
    """意图类型"""
    QUERY = "query"               # 查询意图
    TASK = "task"                 # 任务意图
    DECISION = "decision"         # 决策意图
    LEARNING = "learning"         # 学习意图
    CREATION = "creation"         # 创作意图
    REVIEW = "review"             # 回顾意图
    UNKNOWN = "unknown"           # 未知意图


class ProactiveMemorySystem:
    """
    主动记忆系统 - 让记忆系统具有"预测"和"主动"能力
    
    核心理念：
    1. 预测性：根据上下文预测用户需要什么记忆
    2. 主动性：主动推送相关记忆，而非等待查询
    3. 工作记忆：维护当前上下文相关的高优先级记忆缓冲
    4. 注意力机制：聚焦最相关的记忆，过滤干扰
    
    架构设计：
    ┌─────────────────────────────────────────────────────────────────┐
    │                    PROACTIVE MEMORY SYSTEM                      │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │   Context ──→ Intent Analysis ──→ Memory Prediction             │
    │      │                               │                          │
    │      │                               ▼                          │
    │      │                      ┌──────────────┐                    │
    │      │                      │ WORK MEMORY  │ ← Pre-activation  │
    │      │                      │   BUFFER     │                    │
    │      │                      │ (7±2 slots)  │                    │
    │      │                      └──────┬───────┘                    │
    │      │                             │                            │
    │      ▼                             ▼                            │
    │   User Query ←────────────── Proactive Push                    │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘
    """
    
    # 工作记忆参数（基于认知科学的 7±2 原则）
    WORK_MEMORY_CAPACITY = 7
    WORK_MEMORY_DECAY = 300  # 秒，工作记忆衰减时间
    
    # 预测参数
    PREDICTION_TOP_K = 10
    PUSH_THRESHOLD = 0.6      # 推送阈值
    PREACTIVATION_BOOST = 0.3 # 预激活能量增益
    
    # 意图关键词映射
    INTENT_KEYWORDS = {
        IntentType.QUERY: ['什么', '怎么', '如何', '为什么', '哪个', 'what', 'how', 'why', 'which', '?'],
        IntentType.TASK: ['做', '完成', '实现', '创建', 'build', 'create', 'implement', '完成'],
        IntentType.DECISION: ['选择', '决定', '应该', 'choose', 'decide', 'should'],
        IntentType.LEARNING: ['学习', '理解', '掌握', 'learn', 'understand'],
        IntentType.CREATION: ['写', '生成', '设计', 'write', 'generate', 'design', 'create'],
        IntentType.REVIEW: ['回顾', '总结', '检查', 'review', 'summarize', 'check']
    }
    
    def __init__(self, network: MemoryNeuralNetwork = None,
                 semantic_engine: SemanticMemoryEngine = None):
        """
        初始化主动记忆系统
        
        Args:
            network: 神经网络
            semantic_engine: 语义引擎
        """
        self.network = network
        self.semantic_engine = semantic_engine
        
        # 工作记忆缓冲区
        self.work_memory: Dict[str, WorkMemorySlot] = {}
        
        # 上下文历史（用于预测）
        self.context_history: deque = deque(maxlen=10)
        
        # 预测统计
        self.prediction_stats = {
            'total_predictions': 0,
            'successful_predictions': 0,
            'push_count': 0
        }
        
        # 意图历史
        self.intent_history: List[Tuple[str, IntentType]] = []
    
    def analyze_intent(self, context: str) -> IntentType:
        """
        分析上下文意图
        
        Args:
            context: 当前上下文
        
        Returns:
            意图类型
        """
        context_lower = context.lower()
        
        # 计算各意图的匹配分数
        scores = {}
        for intent_type, keywords in self.INTENT_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in context_lower)
            scores[intent_type] = score
        
        # 选择最高分意图
        if max(scores.values()) > 0:
            best_intent = max(scores, key=scores.get)
        else:
            best_intent = IntentType.UNKNOWN
        
        # 记录意图历史
        self.intent_history.append((context[:50], best_intent))
        
        return best_intent
    
    def predict_needed_memories(self, context: str, 
                                 intent: IntentType = None) -> List[Tuple[str, float]]:
        """
        预测需要的记忆
        
        基于当前上下文和意图，预测用户可能需要的记忆
        
        Args:
            context: 当前上下文
            intent: 意图类型（可选，不传则自动分析）
        
        Returns:
            [(cell_id, relevance), ...]
        """
        # 分析意图
        if intent is None:
            intent = self.analyze_intent(context)
        
        predictions = []
        
        # 方法1：语义相似度预测
        if self.semantic_engine:
            semantic_results = self.semantic_engine.search(
                context, top_k=self.PREDICTION_TOP_K
            )
            for result in semantic_results:
                predictions.append((result['cell_id'], result['similarity']))
        
        # 方法2：意图驱动预测
        intent_predictions = self._predict_by_intent(intent, context)
        for cell_id, relevance in intent_predictions:
            # 合并分数
            existing = next((p for p in predictions if p[0] == cell_id), None)
            if existing:
                # 提升分数
                idx = predictions.index(existing)
                predictions[idx] = (cell_id, min(1.0, existing[1] + relevance * 0.3))
            else:
                predictions.append((cell_id, relevance))
        
        # 方法3：基于上下文历史的预测
        history_predictions = self._predict_by_history(context)
        for cell_id, relevance in history_predictions:
            existing = next((p for p in predictions if p[0] == cell_id), None)
            if existing:
                idx = predictions.index(existing)
                predictions[idx] = (cell_id, min(1.0, existing[1] + relevance * 0.2))
        
        # 排序
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        # 更新统计
        self.prediction_stats['total_predictions'] += 1
        
        return predictions[:self.PREDICTION_TOP_K]
    
    def _predict_by_intent(self, intent: IntentType, context: str) -> List[Tuple[str, float]]:
        """基于意图预测"""
        if not self.network:
            return []
        
        predictions = []
        
        # 根据意图类型筛选记忆
        for cell_id, cell in self.network.cells.items():
            if cell.state == CellState.HIBERNATE:
                continue
            
            relevance = 0.0
            
            # 意图匹配
            if intent == IntentType.QUERY:
                # 查询意图：优先返回语义记忆
                if cell.gene in [CellGene.REFERENCE, CellGene.USER]:
                    relevance = cell.energy * cell.importance
            
            elif intent == IntentType.TASK:
                # 任务意图：优先返回项目记忆
                if cell.gene == CellGene.PROJECT:
                    relevance = cell.energy * cell.importance * 1.2
            
            elif intent == IntentType.DECISION:
                # 决策意图：优先返回反馈记忆
                if cell.gene == CellGene.FEEDBACK:
                    relevance = cell.energy * cell.importance * 1.3
            
            elif intent == IntentType.LEARNING:
                # 学习意图：优先返回高可信度记忆
                relevance = cell.energy * cell.trust_score
            
            elif intent == IntentType.CREATION:
                # 创作意图：返回所有活跃记忆
                relevance = cell.energy
            
            if relevance > 0.3:
                predictions.append((cell_id, relevance))
        
        return predictions
    
    def _predict_by_history(self, context: str) -> List[Tuple[str, float]]:
        """基于历史预测"""
        predictions = []
        
        # 分析历史上下文中的模式
        for past_context in self.context_history:
            # 简单相似度
            overlap = len(set(context.split()) & set(past_context.split()))
            if overlap > 2:
                # 如果与历史上下文相似，可能需要相似的记忆
                # 这里简化处理，实际可以更复杂
                pass
        
        return predictions
    
    def load_to_work_memory(self, cell_id: str, relevance: float, context: str):
        """
        加载记忆到工作记忆缓冲区
        
        模拟人脑的工作记忆机制（容量7±2）
        """
        # 检查容量
        if len(self.work_memory) >= self.WORK_MEMORY_CAPACITY:
            # 移除最不相关的
            min_slot = min(self.work_memory.values(), key=lambda s: s.relevance)
            del self.work_memory[min_slot.cell_id]
        
        # 加载
        self.work_memory[cell_id] = WorkMemorySlot(cell_id, relevance, context)
        
        # 预激活细胞
        if self.network:
            cell = self.network.get_cell(cell_id)
            if cell:
                cell.receive_pulse(self.PREACTIVATION_BOOST)
    
    def get_work_memory(self) -> List[Dict]:
        """获取工作记忆内容"""
        return [
            {
                'cell_id': slot.cell_id,
                'relevance': slot.relevance,
                'context': slot.context,
                'loaded_at': slot.loaded_at,
                'access_count': slot.access_count
            }
            for slot in sorted(
                self.work_memory.values(),
                key=lambda s: s.relevance,
                reverse=True
            )
        ]
    
    def clear_work_memory(self):
        """清空工作记忆"""
        self.work_memory.clear()
    
    def decay_work_memory(self):
        """工作记忆衰减"""
        now = datetime.now()
        to_remove = []
        
        for cell_id, slot in self.work_memory.items():
            loaded_time = datetime.fromisoformat(slot.loaded_at)
            elapsed = (now - loaded_time).total_seconds()
            
            if elapsed > self.WORK_MEMORY_DECAY:
                to_remove.append(cell_id)
            else:
                # 相关性随时间衰减
                decay_factor = 1 - (elapsed / self.WORK_MEMORY_DECAY) * 0.5
                slot.relevance *= decay_factor
        
        for cell_id in to_remove:
            del self.work_memory[cell_id]
    
    def proactive_push(self, context: str) -> List[Dict]:
        """
        主动推送相关记忆
        
        这是核心方法：在用户查询之前，主动推送可能需要的记忆
        
        Args:
            context: 当前上下文
        
        Returns:
            推送的记忆列表
        """
        # 预测
        predictions = self.predict_needed_memories(context)
        
        # 过滤并推送
        pushed = []
        for cell_id, relevance in predictions:
            if relevance >= self.PUSH_THRESHOLD:
                # 加载到工作记忆
                self.load_to_work_memory(cell_id, relevance, context)
                
                # 获取细胞信息
                cell_info = None
                if self.network:
                    cell = self.network.get_cell(cell_id)
                    if cell:
                        cell_info = {
                            'cell_id': cell_id,
                            'content': cell.content[:100],
                            'relevance': round(relevance, 3),
                            'gene': cell.gene.value,
                            'energy': round(cell.energy, 2)
                        }
                
                if cell_info:
                    pushed.append(cell_info)
        
        # 记录上下文历史
        self.context_history.append(context)
        
        # 更新统计
        self.prediction_stats['push_count'] += len(pushed)
        
        return pushed
    
    def update_context(self, context: str):
        """更新上下文"""
        self.context_history.append(context)
        
        # 重新预测并更新工作记忆
        predictions = self.predict_needed_memories(context)
        
        for cell_id, relevance in predictions[:self.WORK_MEMORY_CAPACITY]:
            if cell_id not in self.work_memory:
                self.load_to_work_memory(cell_id, relevance, context)
            else:
                # 更新相关性
                self.work_memory[cell_id].relevance = max(
                    self.work_memory[cell_id].relevance,
                    relevance
                )
    
    def get_prediction_stats(self) -> Dict:
        """获取预测统计"""
        stats = self.prediction_stats.copy()
        stats['work_memory_size'] = len(self.work_memory)
        stats['context_history_size'] = len(self.context_history)
        
        # 计算预测成功率
        if stats['total_predictions'] > 0:
            stats['success_rate'] = stats['successful_predictions'] / stats['total_predictions']
        else:
            stats['success_rate'] = 0
        
        return stats
    
    def mark_prediction_success(self, cell_id: str):
        """标记预测成功"""
        self.prediction_stats['successful_predictions'] += 1
        
        # 提升相关记忆的能量
        if self.network:
            cell = self.network.get_cell(cell_id)
            if cell:
                cell.activate(0.5)
    
    def get_intent_distribution(self) -> Dict[str, int]:
        """获取意图分布统计"""
        distribution = defaultdict(int)
        for _, intent in self.intent_history:
            distribution[intent.value] += 1
        return dict(distribution)
    
    def suggest_next_actions(self, context: str) -> List[str]:
        """
        建议下一步行动
        
        基于上下文和记忆状态，建议可能的行动
        """
        intent = self.analyze_intent(context)
        suggestions = []
        
        if intent == IntentType.QUERY:
            suggestions.append("考虑提供更多上下文以获得更精确的结果")
        
        elif intent == IntentType.TASK:
            # 检查是否有相关的项目记忆
            if self.network:
                project_cells = [
                    c for c in self.network.cells.values()
                    if c.gene == CellGene.PROJECT and c.state == CellState.ACTIVE
                ]
                if project_cells:
                    suggestions.append(f"发现 {len(project_cells)} 个相关项目记忆")
        
        elif intent == IntentType.DECISION:
            suggestions.append("建议回顾相关反馈记忆以辅助决策")
        
        # 检查工作记忆
        if len(self.work_memory) > 0:
            suggestions.append(f"工作记忆中已预加载 {len(self.work_memory)} 个相关记忆")
        
        return suggestions


def main():
    parser = argparse.ArgumentParser(description="Proactive Memory System - 主动记忆系统")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # predict命令
    predict_parser = subparsers.add_parser("predict", help="预测需要的记忆")
    predict_parser.add_argument("--context", required=True, help="当前上下文")
    
    # push命令
    push_parser = subparsers.add_parser("push", help="主动推送记忆")
    push_parser.add_argument("--context", required=True, help="当前上下文")
    
    # intent命令
    intent_parser = subparsers.add_parser("intent", help="分析意图")
    intent_parser.add_argument("--context", required=True, help="上下文")
    
    # work-memory命令
    subparsers.add_parser("work-memory", help="查看工作记忆")
    
    # stats命令
    subparsers.add_parser("stats", help="预测统计")
    
    # suggest命令
    suggest_parser = subparsers.add_parser("suggest", help="建议下一步行动")
    suggest_parser.add_argument("--context", required=True, help="上下文")
    
    args = parser.parse_args()
    
    system = ProactiveMemorySystem()
    
    if args.command == "predict":
        predictions = system.predict_needed_memories(args.context)
        print(f"[PREDICT] Top predictions:")
        for cell_id, relevance in predictions[:5]:
            print(f"  {cell_id}: {relevance:.3f}")
    
    elif args.command == "push":
        pushed = system.proactive_push(args.context)
        print(f"[PUSH] Pushed {len(pushed)} memories:")
        for p in pushed:
            print(f"  {p}")
    
    elif args.command == "intent":
        intent = system.analyze_intent(args.context)
        print(f"[INTENT] Detected intent: {intent.value}")
    
    elif args.command == "work-memory":
        wm = system.get_work_memory()
        print(f"[WORK-MEMORY] {len(wm)} slots:")
        for slot in wm:
            print(f"  {slot}")
    
    elif args.command == "stats":
        stats = system.get_prediction_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    elif args.command == "suggest":
        suggestions = system.suggest_next_actions(args.context)
        print(f"[SUGGEST] Suggestions:")
        for s in suggestions:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
