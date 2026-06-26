#!/usr/bin/env python3
"""
Intent-Aware Recall - 意图感知召回
基于查询意图的多路召回融合
"""

import os
import sys
import json
import time
import argparse
import re
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from enum import Enum
from dataclasses import dataclass

# 导入核心模块
try:
    from memory_core import FluidMemory
    HAS_CORE = True
except ImportError:
    HAS_CORE = False


class QueryIntent(Enum):
    """查询意图类型"""
    FACT = "fact"              # 事实查询："用户叫什么名字"
    DECISION = "decision"      # 决策追溯："为什么选择React"
    PREFERENCE = "preference"  # 偏好确认："用户喜欢什么风格"
    HISTORY = "history"        # 历史追溯："之前讨论过什么"
    STATUS = "status"          # 状态查询："项目进度如何"
    HOWTO = "howto"            # 方法询问："如何配置"
    UNKNOWN = "unknown"


@dataclass
class RecallResult:
    """召回结果"""
    memory_id: str
    content: str
    score: float
    source: str  # 召回来源
    intent_match: float  # 意图匹配度
    metadata: Dict


class IntentClassifier:
    """意图分类器"""
    
    def __init__(self):
        # 意图关键词模式
        self.intent_patterns = {
            QueryIntent.FACT: [
                r'什么是|是什么|叫什么|有哪些|多少',
                r'what is|who is|how many',
                r'用户.*是|角色.*是'
            ],
            QueryIntent.DECISION: [
                r'为什么|为何|原因|决策|选择',
                r'why|reason|decision|choose',
                r'怎么.*决定|为什么.*选'
            ],
            QueryIntent.PREFERENCE: [
                r'喜欢|偏好|想要|希望|习惯',
                r'prefer|like|want|hope',
                r'用户.*风格|回复.*格式'
            ],
            QueryIntent.HISTORY: [
                r'之前|以前|曾经|上次|昨天|上周',
                r'before|previous|last time|yesterday',
                r'讨论过|说过|提到过'
            ],
            QueryIntent.STATUS: [
                r'进度|状态|完成|进行|当前',
                r'progress|status|current|ongoing',
                r'项目.*怎么样|任务.*如何'
            ],
            QueryIntent.HOWTO: [
                r'如何|怎么|怎样|方法|步骤',
                r'how to|how can|steps|method',
                r'怎么.*做|如何.*配置'
            ]
        }
        
        # 类型-意图映射
        self.type_intent_affinity = {
            'user': [QueryIntent.FACT, QueryIntent.PREFERENCE],
            'feedback': [QueryIntent.PREFERENCE, QueryIntent.HOWTO],
            'project': [QueryIntent.DECISION, QueryIntent.STATUS, QueryIntent.HISTORY],
            'reference': [QueryIntent.HOWTO, QueryIntent.FACT]
        }
    
    def classify(self, query: str) -> Tuple[QueryIntent, float]:
        """
        分类查询意图
        
        Args:
            query: 查询文本
        
        Returns:
            (意图类型, 置信度)
        """
        scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, query, re.IGNORECASE):
                    score += 1
            scores[intent] = score
        
        if not scores or max(scores.values()) == 0:
            return QueryIntent.UNKNOWN, 0.0
        
        best_intent = max(scores, key=scores.get)
        confidence = scores[best_intent] / len(self.intent_patterns[best_intent])
        
        return best_intent, min(confidence, 1.0)
    
    def get_preferred_types(self, intent: QueryIntent) -> List[str]:
        """获取意图对应的优先记忆类型"""
        type_priority = []
        
        for mem_type, intents in self.type_intent_affinity.items():
            if intent in intents:
                type_priority.append(mem_type)
        
        # 补充其他类型
        all_types = ['user', 'feedback', 'project', 'reference']
        for t in all_types:
            if t not in type_priority:
                type_priority.append(t)
        
        return type_priority


class MultiPathRecall:
    """多路召回器"""
    
    def __init__(self):
        self.fluid_memory = None
        if HAS_CORE:
            try:
                self.fluid_memory = FluidMemory()
            except Exception:
                pass
    
    def recall_by_vector(self, query: str, limit: int = 10,
                         memory_type: Optional[str] = None) -> List[RecallResult]:
        """向量召回"""
        if not self.fluid_memory:
            return []
        
        results = self.fluid_memory.recall(query, limit, memory_type)
        return [
            RecallResult(
                memory_id=r['id'],
                content=r['content'],
                score=r['score'],
                source='vector',
                intent_match=1.0,
                metadata=r
            )
            for r in results
        ]
    
    def recall_by_keywords(self, query: str, memories: List[Dict],
                           limit: int = 10) -> List[RecallResult]:
        """关键词召回"""
        # 提取查询关键词
        query_words = set(re.findall(r'[\w\u4e00-\u9fff]+', query.lower()))
        
        scored = []
        for m in memories:
            content = m.get('content', '')
            content_words = set(re.findall(r'[\w\u4e00-\u9fff]+', content.lower()))
            
            overlap = len(query_words & content_words)
            if overlap > 0:
                score = overlap / len(query_words) if query_words else 0
                scored.append(RecallResult(
                    memory_id=m.get('id', ''),
                    content=content,
                    score=score,
                    source='keyword',
                    intent_match=1.0,
                    metadata=m
                ))
        
        scored.sort(key=lambda x: -x.score)
        return scored[:limit]
    
    def recall_by_type(self, memory_type: str, 
                       memories: List[Dict],
                       limit: int = 5) -> List[RecallResult]:
        """类型召回"""
        type_memories = [m for m in memories if m.get('type') == memory_type]
        
        return [
            RecallResult(
                memory_id=m.get('id', ''),
                content=m.get('content', ''),
                score=0.5,  # 类型匹配的基础分数
                source='type',
                intent_match=1.0,
                metadata=m
            )
            for m in type_memories[:limit]
        ]
    
    def recall_by_time(self, memories: List[Dict],
                       days: int = 7,
                       limit: int = 10) -> List[RecallResult]:
        """时间召回（近期记忆）"""
        from datetime import datetime, timedelta
        
        cutoff = datetime.now() - timedelta(days=days)
        recent = []
        
        for m in memories:
            created_at = m.get('created_at')
            if created_at:
                try:
                    dt = datetime.fromisoformat(created_at)
                    if dt > cutoff:
                        recent.append((m, dt))
                except Exception:
                    pass
        
        # 按时间排序
        recent.sort(key=lambda x: -x[1].timestamp())
        
        return [
            RecallResult(
                memory_id=m.get('id', ''),
                content=m.get('content', ''),
                score=0.3,
                source='time',
                intent_match=1.0,
                metadata=m
            )
            for m, _ in recent[:limit]
        ]


class IntentAwareRecaller:
    """意图感知召回器"""
    
    def __init__(self):
        self.classifier = IntentClassifier()
        self.multi_path = MultiPathRecall()
        
        # 召回权重配置
        self.recall_weights = {
            QueryIntent.FACT: {'vector': 0.5, 'keyword': 0.3, 'type': 0.2},
            QueryIntent.DECISION: {'vector': 0.4, 'keyword': 0.2, 'type': 0.4},
            QueryIntent.PREFERENCE: {'vector': 0.3, 'keyword': 0.3, 'type': 0.4},
            QueryIntent.HISTORY: {'vector': 0.3, 'keyword': 0.2, 'time': 0.5},
            QueryIntent.STATUS: {'vector': 0.3, 'time': 0.4, 'type': 0.3},
            QueryIntent.HOWTO: {'vector': 0.4, 'keyword': 0.4, 'type': 0.2},
            QueryIntent.UNKNOWN: {'vector': 0.6, 'keyword': 0.4}
        }
    
    def recall(self, query: str, 
               memories: List[Dict] = None,
               limit: int = 10) -> Tuple[List[Dict], Dict]:
        """
        执行意图感知召回
        
        Args:
            query: 查询
            memories: 记忆池（可选，用于非向量召回）
            limit: 返回数量
        
        Returns:
            (召回结果, 召回元信息)
        """
        # 1. 意图分类
        intent, confidence = self.classifier.classify(query)
        
        # 2. 获取召回权重
        weights = self.recall_weights.get(intent, self.recall_weights[QueryIntent.UNKNOWN])
        
        # 3. 获取优先类型
        preferred_types = self.classifier.get_preferred_types(intent)
        
        # 4. 多路召回
        all_results = []
        
        # 向量召回
        if 'vector' in weights and self.multi_path.fluid_memory:
            vector_results = self.multi_path.recall_by_vector(
                query, 
                limit=int(limit * 1.5)
            )
            for r in vector_results:
                r.score *= weights['vector']
                all_results.append(r)
        
        # 关键词召回
        if 'keyword' in weights and memories:
            kw_results = self.multi_path.recall_by_keywords(query, memories, limit)
            for r in kw_results:
                r.score *= weights['keyword']
                all_results.append(r)
        
        # 类型召回
        if 'type' in weights and memories:
            for mem_type in preferred_types[:2]:
                type_results = self.multi_path.recall_by_type(mem_type, memories, limit // 2)
                for r in type_results:
                    r.score *= weights['type']
                    # 类型优先级加成
                    if mem_type == preferred_types[0]:
                        r.score *= 1.2
                    all_results.append(r)
        
        # 时间召回
        if 'time' in weights and memories:
            time_results = self.multi_path.recall_by_time(memories, days=7, limit=limit)
            for r in time_results:
                r.score *= weights['time']
                all_results.append(r)
        
        # 5. 去重合并
        merged = {}
        for r in all_results:
            if r.memory_id in merged:
                # 分数叠加
                merged[r.memory_id].score += r.score * 0.5
            else:
                merged[r.memory_id] = r
        
        # 6. 排序返回
        sorted_results = sorted(merged.values(), key=lambda x: -x.score)[:limit]
        
        # 7. 构建元信息
        meta = {
            'intent': intent.value,
            'intent_confidence': confidence,
            'preferred_types': preferred_types,
            'recall_paths': list(weights.keys()),
            'total_candidates': len(all_results),
            'returned_count': len(sorted_results)
        }
        
        return [
            {
                'id': r.memory_id,
                'content': r.content,
                'score': round(r.score, 4),
                'source': r.source
            }
            for r in sorted_results
        ], meta
    
    def explain_recall(self, query: str, result: Dict, meta: Dict) -> str:
        """解释召回过程"""
        explanation = f"查询意图: {meta['intent']} (置信度: {meta['intent_confidence']:.2f})\n"
        explanation += f"优先类型: {', '.join(meta['preferred_types'][:3])}\n"
        explanation += f"召回路径: {', '.join(meta['recall_paths'])}\n"
        explanation += f"候选数量: {meta['total_candidates']} → 返回 {meta['returned_count']} 条"
        
        return explanation


def main():
    parser = argparse.ArgumentParser(description="Intent-Aware Recall")
    
    parser.add_argument("--query", required=True, help="查询文本")
    parser.add_argument("--limit", type=int, default=5, help="返回数量")
    parser.add_argument("--explain", action="store_true", help="显示召回解释")
    
    args = parser.parse_args()
    
    recaller = IntentAwareRecaller()
    
    # 模拟记忆数据
    sample_memories = [
        {'id': 'm1', 'type': 'user', 'content': '用户是Python开发者，偏好简洁代码风格', 'created_at': datetime.now().isoformat()},
        {'id': 'm2', 'type': 'project', 'content': '项目选择React作为前端框架，因为团队熟悉', 'created_at': datetime.now().isoformat()},
        {'id': 'm3', 'type': 'feedback', 'content': '用户纠正：不要用表格，用列表', 'created_at': datetime.now().isoformat()},
    ]
    
    results, meta = recaller.recall(args.query, sample_memories, args.limit)
    
    print(json.dumps(results, ensure_ascii=False, indent=2))
    
    if args.explain:
        print("\n--- Recall Explanation ---")
        print(recaller.explain_recall(args.query, results[0] if results else {}, meta))


if __name__ == "__main__":
    main()
