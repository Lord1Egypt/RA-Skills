#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
掼蛋出牌策略引擎
基于当前局面、对手出牌、对家配合等因素给出出牌建议
支持AI独立决策模式（信息隔离+性格差异+难度调节）
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class PatternType(Enum):
    """牌型类型"""
    SINGLE = "单张"
    PAIR = "对子"
    TRIPLE = "三张"
    TRIPLE_WITH_PAIR = "三带二"
    STRAIGHT = "顺子"
    PAIR_SEQUENCE = "连对"
    PLANE = "飞机"
    PLANE_WITH_WINGS = "飞机带翅膀"
    BOMB = "炸弹"
    STRAIGHT_FLUSH = "同花顺"
    KING_BOMB = "天王炸弹"
    PASS = "过"


@dataclass
class Card:
    """一张牌"""
    suit: str
    rank: str
    is_joker: bool = False
    is_big_joker: bool = False
    
    def __str__(self) -> str:
        if self.is_joker:
            return f"{'大王' if self.is_big_joker else '小王'}"
        return f"{self.suit}{self.rank}"
    
    @property
    def value(self) -> int:
        """牌面值"""
        rank_values = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                       '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 15}
        if self.is_joker:
            return 100 if self.is_big_joker else 99
        return rank_values.get(self.rank, 0)


@dataclass
class MoveOption:
    """出牌方案"""
    cards: str  # 出牌描述
    pattern: PatternType  # 牌型
    reason: str  # 推荐理由
    risk: str  # 风险提示
    priority: int  # 优先级 1-5
    cooperation_value: int  # 对家配合价值 1-5
    score: int = 0  # 评分 1-10


@dataclass
class AIDecision:
    """AI决策结果"""
    move: str  # 出牌
    thinking: str  # 思考过程
    confidence: float  # 信心度 0-1


class Personality(Enum):
    """AI性格类型"""
    AGGRESSIVE = "aggressive"  # 激进型
    COOPERATIVE = "cooperative"  # 配合型
    CONSERVATIVE = "conservative"  # 保守型
    BALANCED = "balanced"  # 平衡型


class Difficulty(Enum):
    """AI难度"""
    EASY = "初级"
    MEDIUM = "中级"
    HARD = "高级"


class StrategyEngine:
    """出牌策略引擎"""
    
    def __init__(self, hand_cards: List[str], game_state: Dict):
        self.hand_cards = hand_cards
        self.game_state = game_state
        self.level = game_state.get('level', '2')
        self.remaining = game_state.get('remaining_cards', {1: 27, 2: 27, 3: 27, 4: 27})
        self.current_pattern = game_state.get('current_pattern')
        self.last_player = game_state.get('last_player')
        self.is_new_round = game_state.get('is_new_round', True)
        self.current_strength = game_state.get('current_strength', 0)
        
    def analyze_hand(self) -> Dict:
        """分析手牌"""
        analysis = {
            'total': len(self.hand_cards),
            'by_rank': {},
            'by_suit': {},
            'patterns': [],
            'bombs': [],
            'jokers': [],
            'level_cards': []
        }
        
        rank_counts = {}
        suit_counts = {}
        
        for card in self.hand_cards:
            if card in ['大王', '小王']:
                analysis['jokers'].append(card)
                rank_counts[card] = rank_counts.get(card, 0) + 1
            else:
                suit = card[0] if len(card) > 0 and card[0] in '♠♥♣♦' else '?'
                rank = card[1:] if len(card) > 1 else card
                rank_counts[rank] = rank_counts.get(rank, 0) + 1
                suit_counts[suit] = suit_counts.get(suit, 0) + 1
                
                if suit == '♥' and rank == self.level:
                    analysis['level_cards'].append(card)
        
        analysis['by_rank'] = rank_counts
        analysis['by_suit'] = suit_counts
        
        # 识别炸弹
        for rank, count in rank_counts.items():
            if count >= 4:
                analysis['bombs'].append(f"{rank}x{count}")
        
        # 识别可能牌型
        analysis['patterns'] = self._find_patterns(rank_counts, suit_counts)
        
        return analysis
    
    def _find_patterns(self, rank_counts: Dict, suit_counts: Dict) -> List[Dict]:
        """识别手牌中的牌型"""
        patterns = []
        
        # 单张
        singles = [r for r, c in rank_counts.items() if c == 1]
        if singles:
            patterns.append({'type': '单张', 'cards': singles, 'count': len(singles)})
            
        # 对子
        pairs = [r for r, c in rank_counts.items() if c >= 2]
        if pairs:
            patterns.append({'type': '对子', 'cards': pairs, 'count': len(pairs)})
            
        # 三张
        triples = [r for r, c in rank_counts.items() if c >= 3]
        if triples:
            patterns.append({'type': '三张', 'cards': triples, 'count': len(triples)})
            
        # 顺子检测
        ranks = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for i in range(len(ranks) - 4):
            straight = [r for r in ranks[i:i+5] if rank_counts.get(r, 0) >= 1]
            if len(straight) >= 5:
                patterns.append({'type': '顺子', 'cards': straight, 'count': len(straight)})
                
        return patterns
    
    def generate_suggestions(self) -> List[MoveOption]:
        """生成出牌建议"""
        suggestions = []
        
        if self.is_new_round:
            suggestions.extend(self._first_move_suggestions())
        else:
            suggestions.extend(self._follow_up_suggestions())
            
        # 添加评分
        for s in suggestions:
            s.score = self._evaluate_move(s)
            
        # 按评分排序
        suggestions.sort(key=lambda x: x.score, reverse=True)
        
        return suggestions[:3]  # 最多返回3个建议
    
    def _first_move_suggestions(self) -> List[MoveOption]:
        """开局出牌建议"""
        suggestions = []
        analysis = self.analyze_hand()
        
        # 评估手牌强度
        hand_strength = self._evaluate_hand_strength(analysis)
        
        if hand_strength >= 8:
            # 强牌：主动出击
            suggestions.append(MoveOption(
                cards="单张A",
                pattern=PatternType.SINGLE,
                reason="强牌开局，主动控制局面",
                risk="可能暴露牌力",
                priority=5,
                cooperation_value=3
            ))
        elif hand_strength >= 5:
            # 中等牌：试探性出牌
            if analysis['patterns']:
                for p in analysis['patterns']:
                    if p['type'] == '对子' and 'A' in p['cards']:
                        suggestions.append(MoveOption(
                            cards=f"对A",
                            pattern=PatternType.PAIR,
                            reason="强对子开局，争取出牌权",
                            risk="对家可能配合不上",
                            priority=4,
                            cooperation_value=4
                        ))
            
            # 短顺子
            for p in analysis['patterns']:
                if p['type'] == '顺子' and p['count'] <= 6:
                    cards = ''.join(p['cards'][:5])
                    suggestions.append(MoveOption(
                        cards=f"顺子{cards}",
                        pattern=PatternType.STRAIGHT,
                        reason="短顺子试探，不暴露太多牌力",
                        risk="可能被压制",
                        priority=3,
                        cooperation_value=2
                    ))
        else:
            # 弱牌：保守出牌
            singles = analysis['by_rank'].get('3', 0) + analysis['by_rank'].get('4', 0)
            if singles > 0:
                suggestions.append(MoveOption(
                    cards="单张3",
                    pattern=PatternType.SINGLE,
                    reason="弱牌开局，出小牌让对家先打",
                    risk="可能一直被动",
                    priority=2,
                    cooperation_value=5
                ))
        
        # 炸弹建议（任何情况下都可能适用）
        if analysis['bombs']:
            bomb = analysis['bombs'][0]
            suggestions.append(MoveOption(
                cards=f"炸弹{bomb}",
                pattern=PatternType.BOMB,
                reason="关键时刻使用炸弹控制局面",
                risk="用后失去重要控制牌",
                priority=4 if hand_strength < 5 else 3,
                cooperation_value=2
            ))
        
        return suggestions
    
    def _follow_up_suggestions(self) -> List[MoveOption]:
        """跟牌出牌建议"""
        suggestions = []
        analysis = self.analyze_hand()
        
        pattern = self.current_pattern
        strength = self.current_strength
        
        # 能压住的牌
        can_beat = self._find_beatable_cards(analysis, pattern, strength)
        
        for card_info in can_beat[:2]:  # 最多2个压制选项
            suggestions.append(MoveOption(
                cards=card_info['cards'],
                pattern=PatternType(card_info['pattern']),
                reason=card_info['reason'],
                risk=card_info.get('risk', ''),
                priority=card_info.get('priority', 3),
                cooperation_value=card_info.get('coop', 3)
            ))
        
        # 过牌选项
        suggestions.append(MoveOption(
            cards="过",
            pattern=PatternType.PASS,
            reason="对手牌力强，选择观望",
            risk="失去出牌机会",
            priority=1,
            cooperation_value=4
        ))
        
        return suggestions
    
    def _find_beatable_cards(self, analysis: Dict, pattern: str, strength: int) -> List[Dict]:
        """找出能压制的牌"""
        beatable = []
        
        # 简化实现：检查是否能用炸弹压制
        if analysis['bombs']:
            bomb = analysis['bombs'][0]
            beatable.append({
                'cards': f"炸弹{bomb}",
                'pattern': 'BOMB',
                'reason': '用炸弹压制',
                'risk': '消耗重要控制牌',
                'priority': 5 if strength > 15 else 3,
                'coop': 2
            })
        
        # 检查大牌压制
        if pattern == '单张':
            for rank, count in analysis['by_rank'].items():
                if count >= 1:
                    value = self._get_rank_value(rank)
                    if value > strength:
                        beatable.append({
                            'cards': f"单张{rank}",
                            'pattern': 'SINGLE',
                            'reason': f'用{rank}压制',
                            'priority': 4 if value > 14 else 3,
                            'coop': 3
                        })
        
        return beatable
    
    def _get_rank_value(self, rank: str) -> int:
        """获取牌面值"""
        values = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                  '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 15}
        if rank in ['大王']:
            return 100
        if rank in ['小王']:
            return 99
        return values.get(rank, 0)
    
    def _evaluate_hand_strength(self, analysis: Dict) -> int:
        """评估手牌强度"""
        strength = 0
        
        # 王的数量
        strength += len(analysis['jokers']) * 3
        
        # 炸弹数量
        strength += len(analysis['bombs']) * 4
        
        # 大对子
        for rank in ['A', 'K', '2']:
            if analysis['by_rank'].get(rank, 0) >= 2:
                strength += 2
        
        # 级牌
        strength += len(analysis['level_cards']) * 1
        
        # 牌型丰富度
        strength += len(analysis['patterns']) * 0.5
        
        return min(10, int(strength))
    
    def _evaluate_move(self, move: MoveOption) -> int:
        """评估出牌方案得分"""
        score = 5  # 基础分
        
        # 优先级加成
        score += (move.priority - 1) * 0.5
        
        # 配合价值加成
        if '对家' in self.game_state or '3号位' in str(self.game_state):
            score += move.cooperation_value * 0.3
        
        # 炸弹惩罚（不应轻易使用）
        if move.pattern == PatternType.BOMB:
            if self.remaining.get(1, 27) > 15:
                score -= 1
        
        return min(10, max(1, int(score)))


class AIStrategyEngine(StrategyEngine):
    """AI专用策略引擎 - 支持信息隔离和性格差异"""
    
    def __init__(self, hand_cards: List[str], game_state: Dict, 
                 personality: Personality = Personality.BALANCED,
                 difficulty: Difficulty = Difficulty.MEDIUM,
                 seat: int = 1):
        super().__init__(hand_cards, game_state)
        self.personality = personality
        self.difficulty = difficulty
        self.seat = seat
        
        # 性格系数
        self._init_personality_factors()
        
    def _init_personality_factors(self):
        """初始化性格参数"""
        factors = {
            Personality.AGGRESSIVE: {
                'aggression': 1.3,
                'bomb_willingness': 1.4,
                'cooperation': 0.7,
                'risk_taking': 1.2
            },
            Personality.COOPERATIVE: {
                'aggression': 0.8,
                'bomb_willingness': 0.9,
                'cooperation': 1.5,
                'risk_taking': 0.6
            },
            Personality.CONSERVATIVE: {
                'aggression': 0.7,
                'bomb_willingness': 0.8,
                'cooperation': 1.0,
                'risk_taking': 0.5
            },
            Personality.BALANCED: {
                'aggression': 1.0,
                'bomb_willingness': 1.0,
                'cooperation': 1.0,
                'risk_taking': 1.0
            }
        }
        
        self.factors = factors.get(self.personality, factors[Personality.BALANCED])
        
        # 难度系数
        difficulty_factors = {
            Difficulty.EASY: {'accuracy': 0.6, 'memory': 0.5, 'prediction': 0.4},
            Difficulty.MEDIUM: {'accuracy': 0.85, 'memory': 0.75, 'prediction': 0.7},
            Difficulty.HARD: {'accuracy': 1.0, 'memory': 0.95, 'prediction': 0.9}
        }
        
        self.difficulty_factors = difficulty_factors.get(self.difficulty, difficulty_factors[Difficulty.MEDIUM])
    
    def make_decision(self) -> AIDecision:
        """
        AI决策出牌
        关键原则：只使用自己的手牌 + 公共信息，不偷看其他人的牌
        """
        # 基础决策
        suggestions = self.generate_suggestions()
        
        if not suggestions:
            return AIDecision(
                move="过",
                thinking="没有合适的出牌选择，选择过牌",
                confidence=0.9
            )
        
        # 根据性格调整选择
        chosen = self._adjust_by_personality(suggestions)
        
        # 根据难度添加随机性
        chosen = self._add_difficulty_variance(chosen)
        
        # 生成思考过程
        thinking = self._generate_thinking(chosen)
        
        return AIDecision(
            move=chosen.cards,
            thinking=thinking,
            confidence=chosen.score / 10
        )
    
    def _adjust_by_personality(self, suggestions: List[MoveOption]) -> MoveOption:
        """根据性格调整选择"""
        # 过滤掉过牌（激进型不喜欢过）
        if self.personality == Personality.AGGRESSIVE:
            playable = [s for s in suggestions if s.cards != "过"]
            if playable:
                # 激进型更倾向选择高优先级、高炸弹意愿的出牌
                for s in playable:
                    s.score *= self.factors['aggression']
                    if s.pattern == PatternType.BOMB:
                        s.score *= self.factors['bomb_willingness']
                return max(playable, key=lambda x: x.score)
        
        # 配合型优先考虑配合价值
        elif self.personality == Personality.COOPERATIVE:
            for s in suggestions:
                s.score += s.cooperation_value * self.factors['cooperation']
            return max(suggestions, key=lambda x: x.score)
        
        # 保守型倾向于低风险选择
        elif self.personality == Personality.CONSERVATIVE:
            # 给低风险选项加分
            for s in suggestions:
                if '可能' not in s.risk and '暴露' not in s.risk:
                    s.score *= 1.2
            return max(suggestions, key=lambda x: x.score)
        
        # 平衡型按正常评分
        return suggestions[0]
    
    def _add_difficulty_variance(self, chosen: MoveOption) -> MoveOption:
        """根据难度添加随机性"""
        import random
        
        # 初级AI有概率选错
        if self.difficulty == Difficulty.EASY:
            if random.random() > self.difficulty_factors['accuracy']:
                # 选一个次优选项
                return MoveOption(
                    cards="过" if chosen.cards != "过" else chosen.cards,
                    pattern=PatternType.PASS,
                    reason="AI判断失误",
                    risk="",
                    priority=1,
                    cooperation_value=3,
                    score=5
                )
        
        return chosen
    
    def _generate_thinking(self, chosen: MoveOption) -> str:
        """生成AI思考过程说明"""
        if self.personality == Personality.AGGRESSIVE:
            return f"【激进型AI】我选择出{chosen.cards}。当前局面我认为应该主动出击，争取出牌权。"
        elif self.personality == Personality.COOPERATIVE:
            return f"【配合型AI】我选择出{chosen.cards}。这个出牌配合价值{chosen.cooperation_value}分，有利于对家的配合。"
        elif self.personality == Personality.CONSERVATIVE:
            return f"【保守型AI】我选择出{chosen.cards}。我判断当前局面稳妥为主，不宜过于冒进。"
        else:
            return f"【AI】我选择出{chosen.cards}，综合考虑局面后这是最优选择。"
    
    def explain_thinking(self) -> str:
        """返回当前思考过程说明"""
        decision = self.make_decision()
        return decision.thinking


# 辅助函数
def create_ai_engine(seat: int, personality: str, difficulty: str, 
                     hand_cards: List[str], game_state: Dict) -> AIStrategyEngine:
    """创建AI策略引擎"""
    personalities = {
        'aggressive': Personality.AGGRESSIVE,
        'cooperative': Personality.COOPERATIVE,
        'conservative': Personality.CONSERVATIVE,
        '2': Personality.AGGRESSIVE,  # 2号位激进
        '3': Personality.COOPERATIVE,  # 3号位配合
        '4': Personality.CONSERVATIVE  # 4号位保守
    }
    
    difficulties = {
        '初级': Difficulty.EASY,
        '中级': Difficulty.MEDIUM,
        '高级': Difficulty.HARD
    }
    
    pers = personalities.get(personality, Personality.BALANCED)
    diff = difficulties.get(difficulty, Difficulty.MEDIUM)
    
    return AIStrategyEngine(hand_cards, game_state, pers, diff, seat)
