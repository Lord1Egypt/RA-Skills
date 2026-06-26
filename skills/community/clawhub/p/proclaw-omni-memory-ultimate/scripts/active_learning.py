#!/usr/bin/env python3
"""
Active Learning - 主动学习系统
识别重要信息，主动提问确认
"""

import os
import sys
import json
import time
import argparse
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict, Counter
from dataclasses import dataclass
from enum import Enum

# 路径配置
WORKSPACE_ROOT = os.getcwd()
MEMORY_DIR = os.path.join(WORKSPACE_ROOT, "memory")
ACTIVE_LEARNING_PATH = os.path.join(MEMORY_DIR, "active_learning.json")


class ImportanceLevel(Enum):
    """重要性级别"""
    CRITICAL = "critical"    # 必须记住
    HIGH = "high"           # 重要
    MEDIUM = "medium"       # 一般
    LOW = "low"             # 可选


class SignalType(Enum):
    """信号类型"""
    REPETITION = "repetition"      # 重复提及
    EMOTION = "emotion"            # 情感强调
    CORRECTION = "correction"      # 纠正
    EXPLICIT = "explicit"          # 明确要求
    PATTERN = "pattern"            # 模式识别


@dataclass
class LearningSignal:
    """学习信号"""
    content: str
    signal_type: SignalType
    importance: ImportanceLevel
    confidence: float
    context: Dict
    timestamp: str
    action_required: str


class ImportanceDetector:
    """重要性检测器"""
    
    def __init__(self):
        # 明确重要性标记
        self.importance_markers = {
            ImportanceLevel.CRITICAL: [
                r'必须|一定要|千万|绝对|务必',
                r'must|critical|essential|mandatory'
            ],
            ImportanceLevel.HIGH: [
                r'重要|关键|核心|主要|记住|记住这个',
                r'important|key|core|main|remember|note this'
            ],
            ImportanceLevel.MEDIUM: [
                r'比较|有点|稍微|一般',
                r'kind of|somewhat|fairly|moderately'
            ],
            ImportanceLevel.LOW: [
                r'可能|也许|大概|随便|可选',
                r'maybe|perhaps|possibly|optional'
            ]
        }
        
        # 情感强度标记
        self.emotion_markers = {
            'strong_positive': [r'太好了|完美|太棒了|非常好|excellent|perfect|great'],
            'positive': [r'好的|不错|挺好|good|nice|ok'],
            'strong_negative': [r'太糟糕|很差|讨厌|不行|terrible|awful|hate'],
            'negative': [r'不好|不行|不对|bad|wrong']
        }
        
        # 重复追踪
        self.mention_counts: Dict[str, int] = defaultdict(int)
        self.recent_mentions: List[Tuple[str, str]] = []  # (content_hash, timestamp)
    
    def detect(self, content: str, context: Dict = None) -> Tuple[ImportanceLevel, List[SignalType]]:
        """
        检测内容重要性
        
        Args:
            content: 内容
            context: 上下文
        
        Returns:
            (重要性级别, 信号类型列表)
        """
        signals = []
        max_importance = ImportanceLevel.LOW
        
        # 1. 检测明确重要性标记
        for level, patterns in self.importance_markers.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    signals.append(SignalType.EXPLICIT)
                    if self._importance_rank(level) > self._importance_rank(max_importance):
                        max_importance = level
        
        # 2. 检测情感强度
        for emotion_type, patterns in self.emotion_markers.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    signals.append(SignalType.EMOTION)
                    if 'strong' in emotion_type:
                        if self._importance_rank(ImportanceLevel.HIGH) > self._importance_rank(max_importance):
                            max_importance = ImportanceLevel.HIGH
        
        # 3. 检测重复提及
        content_hash = self._hash_content(content)
        self.mention_counts[content_hash] += 1
        self.recent_mentions.append((content_hash, datetime.now().isoformat()))
        
        # 清理旧记录
        cutoff = datetime.now() - timedelta(hours=24)
        self.recent_mentions = [
            (h, t) for h, t in self.recent_mentions 
            if datetime.fromisoformat(t) > cutoff
        ]
        
        if self.mention_counts[content_hash] >= 3:
            signals.append(SignalType.REPETITION)
            if self._importance_rank(ImportanceLevel.HIGH) > self._importance_rank(max_importance):
                max_importance = ImportanceLevel.HIGH
        elif self.mention_counts[content_hash] >= 2:
            signals.append(SignalType.REPETITION)
            if self._importance_rank(ImportanceLevel.MEDIUM) > self._importance_rank(max_importance):
                max_importance = ImportanceLevel.MEDIUM
        
        # 4. 检测纠正
        correction_patterns = [
            r'不是|不对|错了|应该|改为',
            r'wrong|incorrect|should be|instead'
        ]
        for pattern in correction_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                signals.append(SignalType.CORRECTION)
                if self._importance_rank(ImportanceLevel.HIGH) > self._importance_rank(max_importance):
                    max_importance = ImportanceLevel.HIGH
                break
        
        # 5. 模式识别
        if context and context.get('topic_history'):
            topics = context['topic_history']
            if len(topics) >= 3 and len(set(topics[-3:])) == 1:
                signals.append(SignalType.PATTERN)
                max_importance = ImportanceLevel.HIGH
        
        return max_importance, list(set(signals))
    
    def _importance_rank(self, level: ImportanceLevel) -> int:
        """重要性排序值"""
        ranks = {
            ImportanceLevel.CRITICAL: 4,
            ImportanceLevel.HIGH: 3,
            ImportanceLevel.MEDIUM: 2,
            ImportanceLevel.LOW: 1
        }
        return ranks.get(level, 0)
    
    def _hash_content(self, content: str) -> str:
        """内容哈希（简化版）"""
        # 提取关键词作为哈希
        keywords = re.findall(r'[\w\u4e00-\u9fff]+', content.lower())
        return '|'.join(sorted(set(keywords))[:5])


class QuestionGenerator:
    """提问生成器"""
    
    def __init__(self):
        # 提问模板
        self.templates = {
            'user_profile': {
                'trigger_types': ['user'],
                'questions': [
                    "能告诉我更多关于你的技术背景吗？比如常用的编程语言和框架？",
                    "你的工作职责是什么？这样我可以更好地理解你的需求。",
                    "你平时工作会用哪些工具和平台？"
                ]
            },
            'preference': {
                'trigger_types': ['user', 'feedback'],
                'questions': [
                    "对于回复风格，你更喜欢简洁直接还是详细解释？",
                    "你希望我用什么格式展示信息？列表、表格还是代码？",
                    "有没有什么我不应该做的方式？比如格式、语气等？"
                ]
            },
            'project': {
                'trigger_types': ['project'],
                'questions': [
                    "能介绍一下当前项目的主要目标吗？",
                    "项目的关键里程碑和截止日期是什么？",
                    "团队有哪些成员，各自的职责是什么？"
                ]
            },
            'confirmation': {
                'trigger_types': ['*'],
                'questions': [
                    "我理解对吗：{content}？",
                    "让我确认一下，你希望{action}？",
                    "这个信息很重要，我能记录下来吗？"
                ]
            }
        }
    
    def generate(self, signal: LearningSignal, 
                 existing_knowledge: Dict = None) -> List[Dict]:
        """
        生成提问
        
        Args:
            signal: 学习信号
            existing_knowledge: 已有知识
        
        Returns:
            提问列表
        """
        questions = []
        
        # 根据信号类型生成提问
        if signal.signal_type == SignalType.REPETITION:
            questions.append({
                'question': f"我注意到你多次提到这个，这对很重要对吗？",
                'reason': '重复提及通常表示重要性',
                'priority': 1,
                'context': signal.content[:100]
            })
        
        if signal.signal_type == SignalType.CORRECTION:
            questions.append({
                'question': f"我理解了，应该是{signal.content[:50]}，对吗？",
                'reason': '需要确认纠正内容',
                'priority': 1,
                'context': signal.content[:100]
            })
        
        # 根据重要性生成确认
        if signal.importance in [ImportanceLevel.CRITICAL, ImportanceLevel.HIGH]:
            questions.append({
                'question': f"这个信息很重要，我想确认：{signal.content[:80]}？",
                'reason': '高重要性信息需要确认',
                'priority': 2,
                'context': signal.content[:100]
            })
        
        return questions[:3]  # 最多3个问题


class TrustScoreCalculator:
    """可信度计算器"""
    
    def __init__(self):
        self.trust_scores: Dict[str, Dict] = {}
    
    def calculate(self, memory_id: str, 
                  content: str,
                  metadata: Dict = None) -> float:
        """
        计算记忆可信度
        
        可信度因素：
        1. 来源可靠性（用户直接提供 vs 推断）
        2. 确认次数
        3. 时效性
        4. 一致性（与其他记忆是否矛盾）
        5. 访问频率（常被使用的记忆更可信）
        
        Returns:
            可信度分数 (0-1)
        """
        score = 0.5  # 基础分
        
        # 来源可靠性
        if metadata:
            source = metadata.get('source', 'unknown')
            if source == 'user_explicit':
                score += 0.2
            elif source == 'user_implicit':
                score += 0.1
            
            # 确认次数
            confirmations = metadata.get('confirmations', 0)
            score += min(confirmations * 0.1, 0.2)
            
            # 时效性
            created_at = metadata.get('created_at')
            if created_at:
                try:
                    dt = datetime.fromisoformat(created_at)
                    days_old = (datetime.now() - dt).days
                    if days_old < 7:
                        score += 0.1
                    elif days_old > 30:
                        score -= 0.1
                except Exception:
                    pass
            
            # 访问频率
            access_count = metadata.get('access_count', 0)
            score += min(access_count * 0.02, 0.1)
        
        # 存储并返回
        self.trust_scores[memory_id] = {
            'score': max(0, min(1, score)),
            'calculated_at': datetime.now().isoformat()
        }
        
        return round(max(0, min(1, score)), 3)
    
    def detect_drift(self, memory_id: str, 
                     current_content: str,
                     stored_content: str) -> Tuple[bool, float]:
        """
        检测记忆漂移
        
        Args:
            memory_id: 记忆ID
            current_content: 当前内容
            stored_content: 存储内容
        
        Returns:
            (是否有漂移, 漂移程度)
        """
        # 简单的文本相似度
        current_words = set(re.findall(r'[\w\u4e00-\u9fff]+', current_content.lower()))
        stored_words = set(re.findall(r'[\w\u4e00-\u9fff]+', stored_content.lower()))
        
        if not current_words or not stored_words:
            return False, 0.0
        
        jaccard = len(current_words & stored_words) / len(current_words | stored_words)
        drift = 1 - jaccard
        
        return drift > 0.5, drift


class ActiveLearner:
    """主动学习系统"""
    
    def __init__(self):
        self.importance_detector = ImportanceDetector()
        self.question_generator = QuestionGenerator()
        self.trust_calculator = TrustScoreCalculator()
        
        self.pending_signals: List[LearningSignal] = []
        self.learned_items: Dict[str, Dict] = {}
        
        self._load_state()
    
    def _load_state(self):
        """加载状态"""
        if os.path.exists(ACTIVE_LEARNING_PATH):
            try:
                with open(ACTIVE_LEARNING_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.learned_items = data.get('learned', {})
            except Exception:
                pass
    
    def _save_state(self):
        """保存状态"""
        os.makedirs(os.path.dirname(ACTIVE_LEARNING_PATH), exist_ok=True)
        with open(ACTIVE_LEARNING_PATH, 'w', encoding='utf-8') as f:
            json.dump({
                'learned': self.learned_items,
                'pending': [
                    {
                        'content': s.content,
                        'type': s.signal_type.value,
                        'importance': s.importance.value,
                        'timestamp': s.timestamp
                    }
                    for s in self.pending_signals
                ],
                'updated_at': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
    
    def process_input(self, content: str, 
                      context: Dict = None) -> Dict[str, Any]:
        """
        处理用户输入
        
        Args:
            content: 用户输入内容
            context: 上下文
        
        Returns:
            处理结果
        """
        # 检测重要性
        importance, signals = self.importance_detector.detect(content, context)
        
        # 创建学习信号
        signal = LearningSignal(
            content=content,
            signal_type=signals[0] if signals else SignalType.EXPLICIT,
            importance=importance,
            confidence=0.8,
            context=context or {},
            timestamp=datetime.now().isoformat(),
            action_required='store' if importance in [ImportanceLevel.CRITICAL, ImportanceLevel.HIGH] else 'consider'
        )
        
        # 生成提问
        questions = self.question_generator.generate(signal, self.learned_items)
        
        # 决定是否需要主动提问
        should_ask = importance in [ImportanceLevel.CRITICAL, ImportanceLevel.HIGH] or \
                     SignalType.REPETITION in signals or \
                     SignalType.CORRECTION in signals
        
        return {
            'importance': importance.value,
            'signals': [s.value for s in signals],
            'should_ask': should_ask,
            'questions': questions,
            'action': signal.action_required
        }
    
    def confirm_learning(self, content: str, 
                         confirmed: bool = True) -> Dict:
        """
        确认学习
        
        Args:
            content: 内容
            confirmed: 是否确认
        
        Returns:
            学习结果
        """
        content_hash = self.importance_detector._hash_content(content)
        
        if confirmed:
            self.learned_items[content_hash] = {
                'content': content,
                'learned_at': datetime.now().isoformat(),
                'confirmations': 1
            }
        
        self._save_state()
        
        return {
            'confirmed': confirmed,
            'content_hash': content_hash,
            'total_learned': len(self.learned_items)
        }
    
    def get_trust_report(self, memory_id: str,
                         content: str,
                         metadata: Dict = None) -> Dict:
        """
        获取可信度报告
        
        Args:
            memory_id: 记忆ID
            content: 内容
            metadata: 元数据
        
        Returns:
            可信度报告
        """
        trust_score = self.trust_calculator.calculate(memory_id, content, metadata)
        
        return {
            'memory_id': memory_id,
            'trust_score': trust_score,
            'confidence_level': 'high' if trust_score > 0.7 else ('medium' if trust_score > 0.4 else 'low'),
            'factors': {
                'source_reliability': metadata.get('source', 'unknown') if metadata else 'unknown',
                'confirmations': metadata.get('confirmations', 0) if metadata else 0,
                'age_days': (datetime.now() - datetime.fromisoformat(metadata['created_at'])).days if metadata and metadata.get('created_at') else None
            }
        }
    
    def save(self):
        """保存状态"""
        self._save_state()


def main():
    parser = argparse.ArgumentParser(description="Active Learning System")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # process命令
    process_parser = subparsers.add_parser("process", help="处理输入")
    process_parser.add_argument("--content", required=True, help="输入内容")
    
    # confirm命令
    confirm_parser = subparsers.add_parser("confirm", help="确认学习")
    confirm_parser.add_argument("--content", required=True, help="内容")
    confirm_parser.add_argument("--no", action="store_true", help="拒绝")
    
    # trust命令
    trust_parser = subparsers.add_parser("trust", help="可信度评估")
    trust_parser.add_argument("--id", required=True, help="记忆ID")
    trust_parser.add_argument("--content", required=True, help="内容")
    
    # stats命令
    subparsers.add_parser("stats", help="学习统计")
    
    args = parser.parse_args()
    learner = ActiveLearner()
    
    if args.command == "process":
        result = learner.process_input(args.content)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.command == "confirm":
        result = learner.confirm_learning(args.content, confirmed=not args.no)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.command == "trust":
        report = learner.get_trust_report(args.id, args.content)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    elif args.command == "stats":
        print(json.dumps({
            'learned_count': len(learner.learned_items),
            'pending_signals': len(learner.pending_signals)
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
