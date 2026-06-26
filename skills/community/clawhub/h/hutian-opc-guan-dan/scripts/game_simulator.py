#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
掼蛋虚拟对局模拟器
AI随机洗牌发牌、模拟对局、AI身份管理、信息隔离
"""

import random
import json
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class CardPattern(Enum):
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


@dataclass
class Card:
    """一张扑克牌"""
    suit: str  # 花色 ♠♥♣♦
    rank: str  # 点数 3-10,J,Q,K,A,2,王
    is_joker: bool = False
    is_big: bool = False
    
    @property
    def value(self) -> int:
        """获取牌的点数值"""
        rank_values = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                       '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 15}
        if self.is_joker:
            return 100 if self.is_big else 99
        return rank_values.get(self.rank, 0)
    
    def __str__(self) -> str:
        if self.is_joker:
            return f"{'大王' if self.is_big else '小王'}"
        return f"{self.suit}{self.rank}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank and self.is_joker == other.is_joker


@dataclass
class Player:
    """玩家/AI"""
    seat: int  # 座位号 1-4
    role: str  # 角色：user, ai_aggressive, ai_cooperative, ai_conservative
    hand: List[Card] = field(default_factory=list)
    is_user_controlled: bool = False
    
    @property
    def hand_size(self) -> int:
        return len(self.hand)
    
    def remove_cards(self, cards: List[Card]) -> bool:
        """从手牌移除指定的牌"""
        for card in cards:
            if card in self.hand:
                self.hand.remove(card)
            else:
                # 尝试匹配（考虑花色可能不同的情况）
                for c in self.hand:
                    if c.rank == card.rank and c.is_joker == card.is_joker:
                        self.hand.remove(c)
                        break
        return True


@dataclass
class GameRound:
    """一轮出牌"""
    leader: int  # 本轮出牌人
    plays: Dict[int, str] = field(default_factory=dict)  # 各位置出牌
    pattern: Optional[str] = None
    strength: int = 0
    is_complete: bool = False


@dataclass
class GameRecord:
    """游戏记录（用于复盘）"""
    round_number: int
    leader: int
    plays: Dict[int, str]
    current_strength: int
    winner: Optional[int] = None  # 本轮获胜者
    
    def to_dict(self) -> Dict:
        return {
            'round_number': self.round_number,
            'leader': self.leader,
            'plays': self.plays,
            'current_strength': self.current_strength,
            'winner': self.winner
        }


class GameSimulator:
    """虚拟对局模拟器"""
    
    def __init__(self, level: str = '2'):
        self.level = level
        self.players: Dict[int, Player] = {}
        self.deck: List[Card] = []
        self.game_record: List[GameRecord] = []
        self.current_round: Optional[GameRound] = None
        self.current_player: int = 1
        self.round_number: int = 0
        self.game_over: bool = False
        self.winners: List[int] = []  # 排名顺序
        
        # AI难度设置
        self.ai_difficulty: str = "中级"
        
        # AI性格参数
        self.ai_personalities = {
            2: "aggressive",  # 激进型
            3: "cooperative",  # 配合型
            4: "conservative"  # 保守型
        }
        
    def initialize_deck(self) -> List[Card]:
        """初始化108张牌"""
        deck = []
        suits = ['♠', '♥', '♣', '♦']
        ranks = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        # 两副扑克
        for _ in range(2):
            for suit in suits:
                for rank in ranks:
                    deck.append(Card(suit, rank))
        
        # 4张大小王
        deck.append(Card('', '', is_joker=True, is_big=True))
        deck.append(Card('', '', is_joker=True, is_big=True))
        deck.append(Card('', '', is_joker=True, is_big=False))
        deck.append(Card('', '', is_joker=True, is_big=False))
        
        return deck
    
    def shuffle_and_deal(self) -> None:
        """洗牌并发牌"""
        self.deck = self.initialize_deck()
        random.shuffle(self.deck)
        
        # 清空现有玩家手牌
        for seat in range(1, 5):
            if seat not in self.players:
                role = "user" if seat == 1 else f"ai_{self.ai_personalities[seat]}"
                self.players[seat] = Player(seat, role)
            self.players[seat].hand = []
        
        # 发牌：每人27张
        for i in range(108):
            seat = (i % 4) + 1
            self.players[seat].hand.append(self.deck[i])
        
        # 排序手牌
        for seat in range(1, 5):
            self.players[seat].hand.sort(key=lambda c: c.value, reverse=True)
    
    def get_user_hand(self) -> List[str]:
        """获取用户手牌（字符串格式）"""
        return [str(card) for card in self.players[1].hand]
    
    def get_player_hand(self, seat: int) -> List[Card]:
        """获取指定玩家手牌"""
        return self.players[seat].hand
    
    def get_public_info(self) -> Dict:
        """获取公共信息（所有AI可见）"""
        return {
            'level': self.level,
            'round_number': self.round_number,
            'current_player': self.current_player,
            'remaining_cards': {seat: self.players[seat].hand_size for seat in range(1, 5)},
            'played_cards': [r.to_dict() for r in self.game_record],
            'current_round': {
                'leader': self.current_round.leader if self.current_round else None,
                'plays': self.current_round.plays if self.current_round else {},
                'pattern': self.current_round.pattern if self.current_round else None,
                'strength': self.current_round.strength if self.current_round else 0
            } if self.current_round else None
        }
    
    def parse_move(self, move_str: str) -> Tuple[str, List[Card], int]:
        """
        解析出牌字符串
        返回: (牌型, 牌列表, 强度)
        """
        move_str = move_str.strip()
        
        # 解析炸弹
        if '炸弹' in move_str or '炸' in move_str:
            # 提取点数
            rank = None
            for r in ['大王', '小王', '2', 'A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3']:
                if r in move_str:
                    rank = r
                    break
            
            if '大王' in move_str or '小王' in move_str:
                return ('天王炸弹', [], 1000)
            elif rank:
                count = 4  # 默认四炸
                for c in ['七', '六', '五', '四']:
                    if c in move_str:
                        count = {'七': 7, '六': 6, '五': 5, '四': 4}[c]
                        break
                return ('炸弹', [], 500 + count * 10)
        
        # 解析天王炸弹
        if '王炸' in move_str or '王炸' in move_str:
            return ('天王炸弹', [], 1000)
        
        # 解析牌型
        if '单张' in move_str or move_str[0] in '♠♥♣♦':
            return ('单张', [], 14)  # 简化处理
        
        if '对' in move_str:
            return ('对子', [], 14)
        
        if '顺' in move_str:
            return ('顺子', [], 10)
        
        return ('单张', [], 3)
    
    def execute_move(self, seat: int, move_str: str) -> bool:
        """执行出牌"""
        if seat != self.current_player:
            return False
        
        player = self.players[seat]
        pattern, cards, strength = self.parse_move(move_str)
        
        # 验证出牌是否合法（简化版）
        # 实际实现需要更复杂的牌型验证
        
        # 记录出牌
        if self.current_round is None:
            self.current_round = GameRound(leader=seat)
            self.round_number += 1
        
        self.current_round.plays[seat] = move_str
        self.current_round.pattern = pattern
        self.current_round.strength = max(self.current_round.strength, strength)
        
        # 更新当前玩家
        self.current_player = (seat % 4) + 1
        
        # 检查是否一轮结束（所有人都出过牌或有获胜者）
        if len(self.current_round.plays) == 4:
            self.current_round.is_complete = True
            # 确定本轮获胜者（简化处理：最后出牌者获胜）
            self.current_round.winner = seat
            self.game_record.append(self.current_round)
            self.current_round = None
        
        return True
    
    def is_round_over(self) -> bool:
        """检查一轮是否结束"""
        if self.current_round is None:
            return False
        return len(self.current_round.plays) == 4
    
    def get_next_player(self) -> int:
        """获取下一个出牌玩家"""
        return self.current_player
    
    def set_user_control(self, seat: int, controlled: bool = True):
        """设置用户是否控制某个位置"""
        if seat in self.players:
            self.players[seat].is_user_controlled = controlled


class AIStrategy:
    """AI策略引擎"""
    
    def __init__(self, personality: str, difficulty: str = "中级"):
        self.personality = personality
        self.difficulty = difficulty
        
        # 根据性格调整参数
        self.aggression_factor = {
            'aggressive': 1.3,
            'cooperative': 1.0,
            'conservative': 0.7
        }.get(personality, 1.0)
        
        # 根据难度调整参数
        self.difficulty_factor = {
            '初级': 0.6,
            '中级': 1.0,
            '高级': 1.4
        }.get(difficulty, 1.0)
    
    def decide_move(self, hand: List[Card], public_info: Dict, is_new_round: bool) -> str:
        """
        AI决策出牌
        关键原则：只使用自己的手牌 + 公共信息，不偷看其他人的牌
        """
        if not hand:
            return "过"
        
        # 根据性格选择策略
        if self.personality == 'aggressive':
            return self._aggressive_strategy(hand, public_info, is_new_round)
        elif self.personality == 'cooperative':
            return self._cooperative_strategy(hand, public_info, is_new_round)
        elif self.personality == 'conservative':
            return self._conservative_strategy(hand, public_info, is_new_round)
        
        return self._default_strategy(hand, public_info, is_new_round)
    
    def _aggressive_strategy(self, hand: List[Card], public_info: Dict, is_new_round: bool) -> str:
        """激进型策略：喜欢抢出牌权，爱用炸弹"""
        current_round = public_info.get('current_round')
        
        # 新回合：尝试抢打出牌权
        if is_new_round:
            # 优先出能控制局面的牌
            high_cards = [c for c in hand if c.value >= 14]  # A以上
            if high_cards:
                return f"单张{high_cards[0]}"
            
            # 寻找炸弹
            bombs = self._find_bombs(hand)
            if bombs and len(hand) < 15:  # 牌少时更倾向用炸弹
                return f"炸弹{bombs[0]}"
            
            # 出中等牌试探
            medium = [c for c in hand if 8 <= c.value <= 12]
            if medium:
                return f"单张{medium[0]}"
        
        # 跟牌时：积极压制
        if current_round:
            # 优先用炸弹压制
            bombs = self._find_bombs(hand)
            if bombs and len(hand) < 20:
                return f"炸弹{bombs[0]}"
            
            # 尝试压制
            pattern = current_round.get('pattern')
            strength = current_round.get('strength', 0)
            
            # 激进型更愿意出大牌压制
            if strength < 15:
                high = [c for c in hand if c.value > strength]
                if high:
                    return f"单张{high[0]}"
        
        return "过"
    
    def _cooperative_strategy(self, hand: List[Card], public_info: Dict, is_new_round: bool) -> str:
        """配合型策略：优先支持对家，帮挡帮送"""
        current_round = public_info.get('current_round')
        remaining = public_info.get('remaining_cards', {})
        
        # 判断对家(1号位)的状态
        teammate_remaining = remaining.get(1, 27)
        is_teammate_leading = current_round and current_round.get('leader') == 1
        
        # 新回合：对家还没走，让对家先打
        if is_new_round and teammate_remaining > 10:
            # 出小牌让对家先走
            low = [c for c in hand if c.value <= 8]
            if low:
                return f"单张{low[-1]}"
        
        # 跟牌时：帮对家挡牌
        if current_round:
            leader = current_round.get('leader')
            
            # 如果对手在打，压制
            if leader in [2, 4]:
                bombs = self._find_bombs(hand)
                if bombs:
                    return f"炸弹{bombs[0]}"
            
            # 如果对家在打，让对家继续
            if leader == 1:
                return "过"
        
        # 保守出牌
        low = [c for c in hand if c.value <= 10]
        if low:
            return f"单张{low[-1]}"
        
        return "过"
    
    def _conservative_strategy(self, hand: List[Card], public_info: Dict, is_new_round: bool) -> str:
        """保守型策略：擅长防守记牌，后发制人"""
        current_round = public_info.get('current_round')
        
        # 新回合：出小牌探路
        if is_new_round:
            low = [c for c in hand if c.value <= 7]
            if low:
                return f"单张{low[-1]}"
        
        # 跟牌时：后发制人
        if current_round:
            strength = current_round.get('strength', 0)
            
            # 除非必要，不轻易出大牌
            if strength > 12:
                return "过"
            
            # 尝试用小牌压制
            low = [c for c in hand if c.value > strength and c.value <= 10]
            if low:
                return f"单张{low[0]}"
        
        return "过"
    
    def _default_strategy(self, hand: List[Card], public_info: Dict, is_new_round: bool) -> str:
        """默认策略：平衡型"""
        current_round = public_info.get('current_round')
        
        if is_new_round:
            # 出中等牌
            medium = [c for c in hand if 8 <= c.value <= 12]
            if medium:
                return f"单张{medium[0]}"
        
        if current_round:
            strength = current_round.get('strength', 0)
            beats = [c for c in hand if c.value > strength]
            if beats:
                return f"单张{beats[0]}"
        
        return "过"
    
    def _find_bombs(self, hand: List[Card]) -> List[str]:
        """找出手中的炸弹"""
        rank_counts = {}
        for card in hand:
            if not card.is_joker:
                rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1
        
        bombs = [rank for rank, count in rank_counts.items() if count >= 4]
        return bombs
    
    def explain_thinking(self, move: str) -> str:
        """解释AI的思考过程"""
        if self.personality == 'aggressive':
            return f"【激进型AI思考】{move} - 这手牌我选择主动进攻，抢夺出牌权。"
        elif self.personality == 'cooperative':
            return f"【配合型AI思考】{move} - 我在配合对家行动，这手牌帮助队友更好地出牌。"
        elif self.personality == 'conservative':
            return f"【保守型AI思考】{move} - 我在观察局势，这手牌既能控制局面又不暴露太多牌力。"
        return f"【AI思考】{move}"


# 便捷函数：创建模拟器
def create_game(level: str = '2') -> GameSimulator:
    """创建新的游戏模拟器"""
    return GameSimulator(level)


def create_ai(seat: int, difficulty: str = "中级") -> AIStrategy:
    """创建指定位置的AI"""
    personalities = {
        2: "aggressive",
        3: "cooperative",
        4: "conservative"
    }
    return AIStrategy(personalities.get(seat, "aggressive"), difficulty)
