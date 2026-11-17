#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fractal_engine.py — 分形叙事结构引擎

参考：网文创作的系统化工程报告 §5
核心概念：分形叙事 — 全书/卷/章 自相似小循环
每级结构: 开端→发展→高潮→收尾→钩子
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

_log = logging.getLogger("fractal_engine")


@dataclass
class FractalBeat:
    """分形节拍 — 各级叙事的通用模板"""
    phase: str = ""          # 开端/发展/高潮/收尾
    core_event: str = ""
    emotion_payoff: str = ""
    hook: str = ""


@dataclass
class FractalChapter:
    """自相似章节"""
    number: int = 0
    beat: FractalBeat = field(default_factory=FractalBeat)
    word_target: int = 2500


class FractalEngine:
    """分形叙事结构引擎 — 生成各级自相似循环模板"""

    # 全书级分形（大循环）
    BOOK_CYCLE = [
        FractalBeat("开篇崛起", "建立人设+核心矛盾+金手指", "好奇+期待", "长期目标悬念"),
        FractalBeat("中期冲突", "矛盾升级+势力博弈+人设成长", "紧张+爽感交替", "更大危机的暗示"),
        FractalBeat("高潮决战", "各方汇聚+终极对抗+伏笔回收", "震撼+满足", "故事走向的暗示"),
        FractalBeat("结局收尾", "核心矛盾解决+人物归宿+留白", "满足+回味", "番外/续集钩子"),
    ]

    # 分卷级分形（中循环）
    VOLUME_CYCLE = [
        FractalBeat("单元开局", "本卷目标+新地图/新对手", "期待", "卷末伏笔初埋"),
        FractalBeat("冲突积累", "多次小冲突+资源/情报获取", "兴奋", "阶段性胜利"),
        FractalBeat("单元高潮", "本卷核心战斗/冲突", "爽/燃/虐", "跨卷悬念"),
        FractalBeat("卷末收尾", "战果总结+下卷预告", "满足+期待", "下卷钩子"),
    ]

    # 章节级分形（小循环）
    CHAPTER_CYCLE = [
        FractalBeat("开场", "300字内切入场景", "沉浸", "吸引继续读"),
        FractalBeat("推进", "核心事件展开", "投入", "持续兴趣"),
        FractalBeat("转折", "冲突/发现/变故", "情绪波动", "悬念"),
        FractalBeat("收尾", "章末钩子", "好奇+欲罢不能", "下一章动力"),
    ]

    def get_book_template(self, total_volumes: int = 5) -> list:
        """生成全书模板（大循环）"""
        return [{
            "phase": beat.phase,
            "core_event": beat.core_event,
            "emotion": beat.emotion_payoff,
            "volume_range": f"第{i*int(total_volumes/4)+1}-{(i+1)*int(total_volumes/4)}卷",
        } for i, beat in enumerate(self.BOOK_CYCLE[:4])]

    def get_volume_template(self, volume_name: str) -> list:
        """生成单卷模板（中循环）"""
        return [{
            "phase": beat.phase,
            "core_event": beat.core_event,
            "emotion_moment": beat.emotion_payoff,
        } for beat in self.VOLUME_CYCLE]

    def get_chapter_beat(self, position: str) -> Dict:
        """根据章节位置获取对应的分形节拍"""
        phase_map = {
            "开篇300字": self.CHAPTER_CYCLE[0],
            "前1/3": self.CHAPTER_CYCLE[1],
            "中1/3": self.CHAPTER_CYCLE[2],
            "后1/3": self.CHAPTER_CYCLE[3],
        }
        beat = phase_map.get(position, self.CHAPTER_CYCLE[1])
        return {
            "phase": beat.phase,
            "task": beat.core_event,
            "emotion": beat.emotion_payoff,
            "hook": beat.hook,
        }

    def validate_chapter_beat(self, text: str, position: str) -> str:
        """验证章节是否符合同位置的分形要求"""
        beat = self.get_chapter_beat(position)

        # 检查字数
        wc = len(text)
        if position == "开篇300字" and wc > 400:
            return f"[分形] 开篇{wc}字偏长，理想300字内切入"

        # 检查钩子
        if position == "后1/3":
            hook_words = ["突然", "就在这时", "没想到", "?", "？", "发现", "竟然"]
            if not any(hw in text[-200:] for hw in hook_words):
                return "[分形] 章末缺钩子"

        return ""

    def get_cycle_text(self) -> str:
        """获取分形叙事说明文本（用于注入 Prompt）"""
        return (
            "【分形叙事结构】\n"
            "全书 = 大循环: 开篇崛起→中期冲突→高潮决战→结局收尾\n"
            "每卷 = 中循环: 单元开局→冲突积累→单元高潮→卷末收尾\n"
            "每章 = 小循环: 开场(300字)→推进→转折→收尾(钩子)\n"
            "各级结构自相似，确保千万字不跑偏"
        )

    def reset(self):
        pass
