#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
掼蛋复盘引擎
逐手评分、失误分析、口诀沉淀、学习进度追踪
"""

import json
import random
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from collections import defaultdict


@dataclass
class MoveRecord:
    """出牌记录"""
    round_num: int
    move_num: int  # 本轮第几次出牌
    player: int  # 出牌者
    cards: str  # 出的牌
    pattern: str  # 牌型
    strength: int  # 强度
    timestamp: str = ""


@dataclass
class MoveScore:
    """出牌评分"""
    move: MoveRecord
    score: int  # 1-10分
    recommended: str  # 推荐出牌
    reason: str  # 评分理由
    is_correct: bool  # 是否正确
    tags: List[str] = field(default_factory=list)  # 标签：错误类型、亮点类型等


@dataclass
class GameReview:
    """完整复盘报告"""
    game_id: str
    game_result: str  # 胜/负
    upgrade_level: str  # 升级到什么
    key_turning_point: str  # 关键转折点
    move_scores: List[MoveScore]  # 逐手评分
    top_mistakes: List[Dict]  # TOP失误
    top_highlights: List[Dict]  # TOP亮点
    player_score: float  # 综合得分
    player_score_trend: str  # 得分趋势


@dataclass
class LearningProgress:
    """学习进度"""
    total_games: int = 0
    wins: int = 0
    losses: int = 0
    win_rate: float = 0.0
    avg_score: float = 0.0
    score_trend: List[float] = field(default_factory=list)
    
    mistake_types: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    strong_areas: List[str] = field(default_factory=list)
    weak_areas: List[str] = field(default_factory=list)
    
    graduation_progress: float = 0.0  # 毕业进度 0-100%
    consecutive_good_games: int = 0  # 连续好表现局数
    last_5_win_rate: float = 0.0
    
    personal_maxims: List[Dict] = field(default_factory=list)  # 个人口诀
    
    def to_dict(self) -> Dict:
        return asdict(self)


class ScoringRubric:
    """评分标准引擎"""
    
    # 基础分数对照
    SCORE_LEVELS = {
        (9, 10): "最优解",
        (7, 8): "合理选择",
        (5, 6): "可接受",
        (3, 4): "较差",
        (1, 2): "严重失误"
    }
    
    # 失误类型权重
    MISTAKE_WEIGHTS = {
        'bomb_timing': 2.0,      # 炸弹时机
        'pair_sequence': 1.8,   # 顺子拆分
        'cooperation': 2.5,      # 配合失误
        'big_cards': 1.5,        # 大牌提前出
        'passive': 1.2,          # 过于被动
        'aggressive': 1.3,       # 过于激进
        'tribute': 1.0,          # 进贡失误
        'last_play': 2.0,        # 收尾失误
    }
    
    @classmethod
    def get_score_level(cls, score: int) -> str:
        for (low, high), desc in cls.SCORE_LEVELS.items():
            if low <= score <= high:
                return desc
        return "未知"
    
    @classmethod
    def evaluate_single(cls, move: MoveRecord, game_state: Dict) -> MoveScore:
        """评估单张出牌"""
        cards = move.cards
        strength = move.strength
        player = move.player
        remaining = game_state.get('remaining_cards', {})
        my_remaining = remaining.get(player, 27)
        
        score = 7  # 默认7分
        recommended = ""
        reason = ""
        tags = []
        
        # 评估大牌出牌时机
        if strength >= 14:  # A以上
            if my_remaining > 15:
                score = 4
                recommended = "出小牌探路，保留大牌控制"
                reason = f"大牌({cards})出早了，此时你还有{my_remaining}张牌，应保留控制权"
                tags.append('big_cards')
            else:
                score = 8
                reason = "残局出大牌，合理控制局面"
        
        # 评估小牌出牌
        elif strength <= 8:
            if my_remaining > 20:
                score = 8
                reason = "开局出小牌探路，策略正确"
            else:
                score = 6
                reason = "残局出小牌可能给对手送机会"
        
        # 配合价值评估
        if game_state.get('teammate_leading', False):
            if player == 1:  # 用户在配合对家
                if strength <= 10:
                    score = min(score + 1, 10)
                    reason += " | 配合对家出牌，好！"
                    tags.append('cooperation')
        
        return MoveScore(
            move=move,
            score=score,
            recommended=recommended,
            reason=reason,
            is_correct=score >= 7,
            tags=tags
        )
    
    @classmethod
    def evaluate_pair(cls, move: MoveRecord, game_state: Dict) -> MoveScore:
        """评估对子出牌"""
        score = 7
        recommended = ""
        reason = "对子出牌中规中矩"
        tags = []
        
        # 对A评估
        if 'A' in move.cards or 'AA' in move.cards:
            remaining = game_state.get('remaining_cards', {}).get(move.player, 27)
            if remaining > 12:
                score = 5
                recommended = "保留对A作为后手控制"
                reason = "对A是强牌，应留到关键时刻"
                tags.append('big_cards')
        
        # 小对子评估
        if any(r in move.cards for r in ['3', '4', '5']):
            score = 8
            reason = "出小对子探路，策略正确"
        
        return MoveScore(
            move=move,
            score=score,
            recommended=recommended,
            reason=reason,
            is_correct=score >= 7,
            tags=tags
        )
    
    @classmethod
    def evaluate_straight(cls, move: MoveRecord, game_state: Dict) -> MoveScore:
        """评估顺子出牌"""
        score = 7
        recommended = ""
        reason = "顺子出牌选择"
        tags = []
        
        # 评估长顺子
        if '顺' in move.pattern:
            straight_length = cls._count_straight_length(move.cards)
            if straight_length >= 8:
                score = 5
                recommended = "拆分顺子，保留关键牌"
                reason = f"长顺子({straight_length}张)出完会暴露牌力"
                tags.append('pair_sequence')
        
        # 短顺子评估
        if straight_length <= 5:
            score = 8
            reason = "短顺子试探，不暴露太多牌力"
        
        return MoveScore(
            move=move,
            score=score,
            recommended=recommended,
            reason=reason,
            is_correct=score >= 7,
            tags=tags
        )
    
    @classmethod
    def evaluate_bomb(cls, move: MoveRecord, game_state: Dict) -> MoveScore:
        """评估炸弹出牌"""
        score = 7
        recommended = ""
        reason = "炸弹使用"
        tags = []
        
        remaining = game_state.get('remaining_cards', {}).get(move.player, 27)
        
        # 评估炸弹时机
        if '天王' in move.cards or '王炸' in move.cards:
            if remaining > 10:
                score = 6
                reason = "天王炸弹过早使用"
            else:
                score = 9
                reason = "关键时刻使用天王炸弹收尾"
                tags.append('highlight')
        else:
            # 普通炸弹
            if remaining > 15:
                score = 5
                recommended = "保留炸弹在关键时刻使用"
                reason = "牌多时过早使用炸弹"
                tags.append('bomb_timing')
            elif remaining < 8:
                score = 9
                reason = "残局用炸弹收尾，时机恰当"
                tags.append('highlight')
            else:
                # 中期炸弹
                if game_state.get('opponent_leading', False):
                    score = 9
                    reason = "压制对手出牌，使用炸弹正确"
                    tags.append('highlight')
                else:
                    score = 6
                    reason = "中期用炸弹需谨慎"
        
        return MoveScore(
            move=move,
            score=score,
            recommended=recommended,
            reason=reason,
            is_correct=score >= 7,
            tags=tags
        )
    
    @classmethod
    def _count_straight_length(cls, cards: str) -> int:
        """计算顺子长度"""
        # 简化实现
        return len([c for c in cards if c.isdigit() or c in 'JQKA'])
    
    @classmethod
    def evaluate_pass(cls, move: MoveRecord, game_state: Dict) -> MoveScore:
        """评估过牌"""
        score = 7
        reason = "选择过牌"
        tags = []
        
        current_strength = game_state.get('current_strength', 0)
        player_hand_value = game_state.get('player_hand_value', 10)
        
        if current_strength > player_hand_value:
            score = 8
            reason = "明智选择，对手牌力过强"
            tags.append('highlight')
        elif current_strength < 10 and player_hand_value > 12:
            score = 5
            reason = "可以尝试压制，不必过牌"
            tags.append('passive')
        
        return MoveScore(
            move=move,
            score=score,
            recommended="",
            reason=reason,
            is_correct=score >= 7,
            tags=tags
        )


class MaximGenerator:
    """口诀生成器"""
    
    # 常见失误对应的口诀
    MAXIMS = {
        'big_cards': [
            "大对留后手，小对先探路",
            "大牌晚出是高手，大牌早出是菜鸟",
            "A以上要稳住，冲动是魔鬼"
        ],
        'bomb_timing': [
            "炸弹不拆牌，整手压到底",
            "炸弹用在关键时，不是随便就能使",
            "前期忍一忍，后期炸弹震"
        ],
        'cooperation': [
            "对家在冲刺，我方必挡牌",
            "对家报单我先过，让他先跑我断后",
            "帮对家挡牌是美德，帮对家送牌是智慧"
        ],
        'pair_sequence': [
            "顺子不拆打，拆了要后悔",
            "长顺留一手，短顺先出手"
        ],
        'passive': [
            "该出手时就出手，不要只会跟着走",
            "过于保守难取胜，适度激进是真理"
        ],
        'aggressive': [
            "激进有度，冒进无路",
            "抢牌要看实力，没实力就老实"
        ],
        'highlight': [
            "好牌用在刀刃上，时机把握真叫棒",
            "关键时刻敢出手，这才是真高手"
        ]
    }
    
    @classmethod
    def get_maxim(cls, mistake_type: str) -> str:
        """获取特定失误类型的口诀"""
        maxims = cls.MAXIMS.get(mistake_type, [])
        if maxims:
            return random.choice(maxims)
        return "熟能生巧，多练多得"
    
    @classmethod
    def generate_summary_maxims(cls, mistakes: List[str]) -> List[str]:
        """根据失误类型生成总结口诀"""
        result = []
        for mistake in mistakes[:3]:  # 最多3条
            maxim = cls.get_maxim(mistake)
            if maxim not in result:
                result.append(maxim)
        return result


class ReviewEngine:
    """复盘引擎主类"""
    
    def __init__(self):
        self.current_game_record: List[MoveRecord] = []
        self.learning_progress = LearningProgress()
        self._load_progress()
    
    def _load_progress(self):
        """加载学习进度"""
        try:
            with open('./.skills/胡田-OPC导师-掼蛋助手Skill/data/progress.json', 'r') as f:
                data = json.load(f)
                self.learning_progress = LearningProgress(**data)
        except:
            pass
    
    def _save_progress(self):
        """保存学习进度"""
        import os
        os.makedirs('./.skills/胡田-OPC导师-掼蛋助手Skill/data', exist_ok=True)
        with open('./.skills/胡田-OPC导师-掼蛋助手Skill/data/progress.json', 'w') as f:
            json.dump(self.learning_progress.to_dict(), f, ensure_ascii=False, indent=2)
    
    def record_move(self, move: MoveRecord):
        """记录一次出牌"""
        self.current_game_record.append(move)
    
    def evaluate_game(self, game_result: str, upgrade_level: str) -> GameReview:
        """评估整局游戏"""
        game_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 评估每一步
        move_scores = []
        for move in self.current_game_record:
            if move.player != 1:  # 只评估用户(1号位)的出牌
                continue
            
            game_state = self._build_game_state(move)
            
            if '过' in move.cards:
                score = ScoringRubric.evaluate_pass(move, game_state)
            elif '炸' in move.cards:
                score = ScoringRubric.evaluate_bomb(move, game_state)
            elif '顺' in move.cards:
                score = ScoringRubric.evaluate_straight(move, game_state)
            elif '对' in move.cards:
                score = ScoringRubric.evaluate_pair(move, game_state)
            else:
                score = ScoringRubric.evaluate_single(move, game_state)
            
            move_scores.append(score)
        
        # 找出TOP失误和亮点
        top_mistakes = self._find_top_mistakes(move_scores)
        top_highlights = self._find_top_highlights(move_scores)
        
        # 计算综合得分
        player_score = sum(ms.score for ms in move_scores) / len(move_scores) if move_scores else 0
        
        # 生成复盘报告
        review = GameReview(
            game_id=game_id,
            game_result=game_result,
            upgrade_level=upgrade_level,
            key_turning_point=self._find_key_turning_point(move_scores),
            move_scores=move_scores,
            top_mistakes=top_mistakes,
            top_highlights=top_highlights,
            player_score=player_score,
            player_score_trend="上升" if player_score > self.learning_progress.avg_score else "下降"
        )
        
        # 更新学习进度
        self._update_progress(game_result, player_score, move_scores, top_mistakes)
        
        return review
    
    def _build_game_state(self, move: MoveRecord) -> Dict:
        """构建游戏状态供评估使用"""
        game_state = {
            'remaining_cards': {},
            'current_strength': move.strength,
            'player_hand_value': move.strength,
        }
        
        # 根据出牌序号估算剩余牌数
        move_index = self.current_game_record.index(move) if move in self.current_game_record else 0
        estimated_played = move_index // 4
        
        for player in range(1, 5):
            rounds_played = estimated_played - (player > (move.player + (move_index % 4)) % 4 and move_index % 4 != 0)
            game_state['remaining_cards'][player] = max(27 - rounds_played * 4, 1)
        
        return game_state
    
    def _find_top_mistakes(self, move_scores: List[MoveScore]) -> List[Dict]:
        """找出TOP失误"""
        mistakes = [ms for ms in move_scores if ms.score < 5]
        mistakes.sort(key=lambda x: x.score)
        
        result = []
        for ms in mistakes[:3]:
            mistake_dict = {
                'move': f"第{ms.move.round_num}轮第{ms.move.move_num}手",
                'actual': ms.move.cards,
                'score': ms.score,
                'recommended': ms.recommended,
                'reason': ms.reason,
                'type': ms.tags[0] if ms.tags else 'other',
                'maxim': MaximGenerator.get_maxim(ms.tags[0] if ms.tags else 'other')
            }
            result.append(mistake_dict)
        
        return result
    
    def _find_top_highlights(self, move_scores: List[MoveScore]) -> List[Dict]:
        """找出TOP亮点"""
        highlights = [ms for ms in move_scores if ms.score >= 9]
        
        result = []
        for ms in highlights[:3]:
            highlight_dict = {
                'move': f"第{ms.move.round_num}轮第{ms.move.move_num}手",
                'actual': ms.move.cards,
                'score': ms.score,
                'reason': ms.reason
            }
            result.append(highlight_dict)
        
        return result
    
    def _find_key_turning_point(self, move_scores: List[MoveScore]) -> str:
        """找出关键转折点"""
        if not move_scores:
            return "无明显转折点"
        
        # 找到评分最低的点作为转折点
        worst = min(move_scores, key=lambda x: x.score)
        return f"第{worst.move.round_num}轮，{worst.move.cards}，局势发生逆转"
    
    def _update_progress(self, game_result: str, player_score: float, 
                         move_scores: List[MoveScore], top_mistakes: List[Dict]):
        """更新学习进度"""
        # 更新基本信息
        self.learning_progress.total_games += 1
        if '胜' in game_result:
            self.learning_progress.wins += 1
        else:
            self.learning_progress.losses += 1
        
        self.learning_progress.win_rate = self.learning_progress.wins / self.learning_progress.total_games * 100
        
        # 更新得分趋势
        self.learning_progress.score_trend.append(player_score)
        if len(self.learning_progress.score_trend) > 20:
            self.learning_progress.score_trend = self.learning_progress.score_trend[-20:]
        
        self.learning_progress.avg_score = sum(self.learning_progress.score_trend) / len(self.learning_progress.score_trend)
        
        # 更新失误类型统计
        for mistake in top_mistakes:
            mistake_type = mistake.get('type', 'other')
            self.learning_progress.mistake_types[mistake_type] += 1
        
        # 找出薄弱环节和强项
        if self.learning_progress.mistake_types:
            sorted_mistakes = sorted(self.learning_progress.mistake_types.items(), key=lambda x: x[1], reverse=True)
            self.learning_progress.weak_areas = [m[0] for m in sorted_mistakes[:3]]
        
        # 计算毕业进度
        self._calculate_graduation_progress()
        
        # 保存进度
        self._save_progress()
    
    def _calculate_graduation_progress(self):
        """计算毕业进度"""
        # 毕业条件：连续5局胜率>60%且无重大失误
        recent_games = self.learning_progress.score_trend[-5:] if len(self.learning_progress.score_trend) >= 5 else self.learning_progress.score_trend
        
        if len(recent_games) < 5:
            self.learning_progress.graduation_progress = len(recent_games) * 20
            return
        
        # 计算最近5局的胜率和失误
        recent_mistakes = sum(1 for ms in self.learning_progress.score_trend[-5:] if ms < 5)
        good_games = sum(1 for s in recent_games if s >= 6)
        
        if good_games >= 3 and recent_mistakes <= 2:
            self.learning_progress.consecutive_good_games += 1
        else:
            self.learning_progress.consecutive_good_games = 0
        
        # 毕业进度
        self.learning_progress.graduation_progress = min(100, 
            (self.learning_progress.consecutive_good_games / 5) * 40 +
            (self.learning_progress.win_rate / 100) * 30 +
            ((10 - len(self.learning_progress.weak_areas)) / 10) * 30
        )
    
    def generate_review_report(self, review: GameReview) -> str:
        """生成复盘报告（文本格式）"""
        report = f"""
=== 第{self.learning_progress.total_games}局复盘 ===
结果：我方{review.game_result}，升级至{review.upgrade_level}
关键转折：{review.key_turning_point}

【逐手评分】
"""
        for ms in review.move_scores:
            icon = "✅" if ms.score >= 8 else ("❌" if ms.score < 5 else "")
            report += f"第{ms.move.round_num}手：你出 {ms.move.cards} → {ms.score}分（{ms.reason}）{icon}\n"
            if ms.recommended:
                report += f"  → 推荐：{ms.recommended}\n"
        
        report += "\n【失误TOP3】\n"
        for i, mistake in enumerate(review.top_mistakes, 1):
            report += f"{i}. {mistake['move']}：{mistake['actual']} → {mistake['reason']}\n"
            report += f"   口诀：{mistake['maxim']}\n"
        
        if review.top_highlights:
            report += "\n【亮点时刻】\n"
            for highlight in review.top_highlights:
                report += f"✨ 第{highlight['move']}：{highlight['actual']} - {highlight['reason']}\n"
        
        report += f"""
【学习进度】
累计对局：{self.learning_progress.total_games}局 | 胜率：{self.learning_progress.win_rate:.1f}% {review.player_score_trend}
平均得分：{self.learning_progress.avg_score:.1f}
薄弱环节：{', '.join(self.learning_progress.weak_areas) if self.learning_progress.weak_areas else '暂无明显薄弱'}
毕业进度：{self._get_progress_bar()} {self.learning_progress.graduation_progress:.0f}%
"""
        
        return report
    
    def _get_progress_bar(self) -> str:
        """获取进度条"""
        filled = int(self.learning_progress.graduation_progress // 10)
        return "■" * filled + "□" * (10 - filled)
    
    def get_progress_report(self) -> str:
        """获取进度报告"""
        return f"""
╔══════════════════════════════════════╗
║        🎯 学习进度报告              ║
╠══════════════════════════════════════╣
║  累计对局：{self.learning_progress.total_games}局                    ║
║  胜率：{self.learning_progress.win_rate:.1f}%                      ║
║  平均得分：{self.learning_progress.avg_score:.1f}                       ║
║  得分趋势：{review.player_score_trend if 'review' in dir() else '上升'}                       ║
╠══════════════════════════════════════╣
║  📊 薄弱环节                       ║
║  {', '.join(self.learning_progress.weak_areas[:2]) if self.learning_progress.weak_areas else '暂无明显薄弱'}              ║
╠══════════════════════════════════════╣
║  🎓 毕业进度                       ║
║  {self._get_progress_bar()}  {self.learning_progress.graduation_progress:.0f}%            ║
╚══════════════════════════════════════╝
"""
    
    def clear_current_game(self):
        """清除当前游戏记录"""
        self.current_game_record = []


# 便捷函数
def create_review_engine() -> ReviewEngine:
    """创建复盘引擎"""
    return ReviewEngine()
