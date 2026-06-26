#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
掼蛋记牌器核心模块
追踪108张牌的状态，支持实战模式和虚拟对局
"""

import json
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum


class GameMode(Enum):
    """游戏模式"""
    REAL = "实战"  # 实战模式
    TRAINING = "陪练"  # 陪练模式
    SPECTATING = "观战"  # 观战模式


class Card:
    """一张扑克牌"""
    SUITS = ['♠', '♥', '♣', '♦']  # 黑桃、红桃、草花、方块
    RANKS = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
    RANKS_ENCODED = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
                     '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 15}
    
    def __init__(self, suit: str, rank: str, is_joker: bool = False, is_big: bool = False):
        self.suit = suit
        self.rank = rank
        self.is_joker = is_joker
        self.is_big = is_big
        
    @property
    def rank_value(self) -> int:
        """获取牌的点数值"""
        if self.is_joker:
            return 100 if self.is_big else 99
        return self.RANKS_ENCODED.get(self.rank, 0)
    
    def __str__(self) -> str:
        if self.is_joker:
            return f"{'大王' if self.is_big else '小王'}"
        return f"{self.suit}{self.rank}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank and self.is_joker == other.is_joker


@dataclass
class GameState:
    """游戏状态"""
    level: str = '2'
    current_player: int = 1
    deck_leader: int = 1
    current_pattern: Optional[str] = None
    current_strength: int = 0
    remaining_cards: Dict[int, int] = field(default_factory=lambda: {1: 27, 2: 27, 3: 27, 4: 27})
    played_cards: Dict[int, List[str]] = field(default_factory=lambda: defaultdict(list))
    hand_cards: Dict[int, Set[str]] = field(default_factory=lambda: defaultdict(set))
    round_cards: Dict[int, str] = field(default_factory=lambda: {})
    is_new_round: bool = True
    game_mode: GameMode = GameMode.REAL
    round_number: int = 0
    
    # 虚拟对局专用
    all_known_cards: Set[str] = field(default_factory=set)  # 已知的牌（通过出牌推断）
    ai_hands: Dict[int, Set[str]] = field(default_factory=lambda: defaultdict(set))  # AI手牌（仅陪练模式可见）
    
    def __post_init__(self):
        for i in range(1, 5):
            if i not in self.hand_cards:
                self.hand_cards[i] = set()
            if i not in self.ai_hands:
                self.ai_hands[i] = set()


class CardTracker:
    """记牌器"""
    
    def __init__(self, mode: GameMode = GameMode.REAL):
        self.state = GameState()
        self.state.game_mode = mode
        self.all_cards = self._init_deck()
        self.move_history: List[Dict] = []  # 移动历史（用于复盘）
        
    def _init_deck(self) -> List[str]:
        """初始化108张牌"""
        cards = []
        for _ in range(2):
            for suit in Card.SUITS:
                for rank in Card.RANKS:
                    cards.append(f"{suit}{rank}")
        cards.extend(['大王', '大王', '小王', '小王'])
        return cards
    
    def set_mode(self, mode: GameMode):
        """设置游戏模式"""
        self.state.game_mode = mode
    
    def set_level(self, level: str):
        """设置当前级牌"""
        self.state.level = level
        self.state.level_cards = [f"♥{level}", f"♥{level}"]
    
    def set_hand(self, cards: List[str]):
        """设置用户手牌"""
        self.state.hand_cards[1] = set(cards)
        self.state.remaining_cards[1] = len(cards)
        for card in cards:
            if card in self.all_cards:
                self.all_cards.remove(card)
    
    def set_ai_hand(self, seat: int, cards: List[str]):
        """设置AI手牌（仅陪练/观战模式）"""
        if self.state.game_mode in [GameMode.TRAINING, GameMode.SPECTATING]:
            self.state.ai_hands[seat] = set(cards)
            for card in cards:
                if card in self.all_cards:
                    self.all_cards.remove(card)
    
    def add_hand_cards(self, cards: List[str]):
        """添加到手牌（摸牌）"""
        for card in cards:
            self.state.hand_cards[1].add(card)
            self.state.remaining_cards[1] = len(self.state.hand_cards[1])
            if card in self.all_cards:
                self.all_cards.remove(card)
    
    def play_card(self, player: int, cards: str) -> bool:
        """记录玩家出牌"""
        if player < 1 or player > 4:
            return False
            
        card_list = self._parse_cards(cards)
        self.state.remaining_cards[player] -= len(card_list)
        
        self.state.played_cards[player].append(cards)
        
        for card in card_list:
            if card in self.all_cards:
                self.all_cards.remove(card)
            if card in self.state.hand_cards[player]:
                self.state.hand_cards[player].remove(card)
            if card in self.state.ai_hands.get(player, set()):
                self.state.ai_hands[player].remove(card)
            
            # 记录为已知牌
            self.state.all_known_cards.add(card)
        
        if self.state.is_new_round:
            self.state.deck_leader = player
            self.state.is_new_round = False
            self.state.current_pattern = self._identify_pattern(cards)
            self.state.current_strength = self._get_strength(cards)
            self.state.round_number += 1
        else:
            if self._can_beat(cards, self.state.current_pattern, self.state.current_strength):
                self.state.current_strength = self._get_strength(cards)
        
        self.state.round_cards[player] = cards
        
        # 记录移动历史
        self.move_history.append({
            'round': self.state.round_number,
            'player': player,
            'cards': cards,
            'pattern': self.state.current_pattern,
            'strength': self.state.current_strength,
            'is_leader': player == self.state.deck_leader
        })
        
        return True
    
    def _parse_cards(self, cards: str) -> List[str]:
        """解析出牌字符串"""
        card_list = []
        cards = cards.strip()
        
        if '炸' in cards:
            # 炸弹处理
            return [cards]
        
        if '顺' in cards:
            # 顺子处理
            ranks = [c for c in cards if c.isdigit() or c in 'JQKA']
            suits = [c for c in cards if c in '♠♥♣♦']
            if len(ranks) == len(suits):
                return [f"{s}{r}" for s, r in zip(suits, ranks)]
            return [cards]
        
        if '对' in cards:
            rank = cards.replace('对', '').strip()
            return [f"♠{rank}", f"♥{rank}"]
        
        # 单张
        if len(cards) >= 2:
            return [cards]
        
        return [cards]
    
    def _identify_pattern(self, cards: str) -> str:
        """识别牌型"""
        if '炸' in cards:
            return '炸弹'
        if '顺' in cards:
            return '顺子'
        if '对' in cards:
            return '对子'
        if '三带' in cards:
            return '三带二'
        return '单张'
    
    def _get_strength(self, cards: str) -> int:
        """获取出牌强度"""
        rank_values = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                       '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 15}
        
        if '天王' in cards or '王炸' in cards:
            return 1000
        if '炸' in cards:
            return 500
        
        rank = None
        for r in ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']:
            if r in cards:
                rank = r
                break
        
        if rank:
            return rank_values.get(rank, 5)
        
        if '大王' in cards:
            return 100
        if '小王' in cards:
            return 99
        
        return 5
    
    def _can_beat(self, cards: str, pattern: str, strength: int) -> bool:
        """判断是否能压过"""
        if self.state.current_pattern is None:
            return True
        
        if '炸' in cards:
            return True
        
        if pattern == '炸弹':
            return False
        
        return self._get_strength(cards) > strength
    
    def pass_card(self, player: int) -> bool:
        """记录过牌"""
        self.state.round_cards[player] = "过"
        
        self.move_history.append({
            'round': self.state.round_number,
            'player': player,
            'cards': '过',
            'pattern': self.state.current_pattern,
            'strength': self.state.current_strength,
            'is_leader': False
        })
        
        # 检查是否一轮结束
        if len(self.state.round_cards) == 4:
            self.state.is_new_round = True
            self.state.round_cards = {}
            self.state.current_pattern = None
            self.state.current_strength = 0
        
        return True
    
    def get_remaining_cards(self) -> Dict[str, int]:
        """获取剩余牌统计"""
        remaining = {}
        for card in self.all_cards:
            remaining[card] = remaining.get(card, 0) + 1
        
        # 减去已知已出的牌
        for card in self.state.all_known_cards:
            if card in remaining:
                remaining[card] = max(0, remaining[card] - 1)
        
        return remaining
    
    def get_played_cards_summary(self) -> Dict[int, List[str]]:
        """获取已出牌汇总"""
        return dict(self.state.played_cards)
    
    def get_user_hand(self) -> Set[str]:
        """获取用户手牌"""
        return self.state.hand_cards[1]
    
    def get_ai_hand(self, seat: int) -> Set[str]:
        """获取AI手牌（陪练/观战模式）"""
        if self.state.game_mode in [GameMode.TRAINING, GameMode.SPECTATING]:
            return self.state.ai_hands.get(seat, set())
        return set()
    
    def reset(self):
        """重置记牌器"""
        self.state = GameState()
        self.state.game_mode = self.state.game_mode  # 保持模式
        self.all_cards = self._init_deck()
        self.move_history = []
    
    def get_game_state_summary(self) -> Dict:
        """获取游戏状态摘要"""
        return {
            'level': self.state.level,
            'current_player': self.state.current_player,
            'round_number': self.state.round_number,
            'remaining_cards': self.state.remaining_cards,
            'current_pattern': self.state.current_pattern,
            'current_strength': self.state.current_strength,
            'is_new_round': self.state.is_new_round,
            'game_mode': self.state.game_mode.value
        }
    
    def export_history(self) -> List[Dict]:
        """导出移动历史（用于复盘）"""
        return self.move_history
    
    def import_history(self, history: List[Dict]):
        """导入移动历史"""
        self.move_history = history
        # 重放历史以重建状态
        self.reset()
        for move in history:
            if move['cards'] == '过':
                self.pass_card(move['player'])
            else:
                self.play_card(move['player'], move['cards'])
