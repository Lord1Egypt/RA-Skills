#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agent_coordinator.py — 多智能体协调器

参考：《网络小说全维度创新创作与AI工业化稳态落地深度研究报告（进阶迭代版）》
第3章 AI多智能体&子代理全维度创作体系

将 pipeline 的串行生成流程映射到 7 大核心智能体的分工体系。
当前为轻量级协调版本，各智能体直接调用对应的引擎实例。
"""

import logging
from typing import Dict, Any, List, Optional

_log = logging.getLogger("agent_coordinator")


class AgentCoordinator:
    """多智能体协调器 — 统筹7大核心智能体的调用"""

    # 7 大核心智能体映射
    AGENT_MAP = {
        "world": {"name": "世界观统筹", "engine": "worldbuilder", "identity_key": "story_architect"},
        "character": {"name": "人设动态管控", "engine": "novel_state", "identity_key": "detail_agent"},
        "plot": {"name": "剧情节奏推演", "engine": ["engines_tension", "engines_planning"], "identity_key": "critic"},
        "foreshadow": {"name": "伏笔埋点闭环", "engine": "arc_manager", "identity_key": "story_architect"},
        "style": {"name": "文笔拟人化润色", "engine": "writing_notes", "identity_key": "style_master"},
        "emotion": {"name": "情绪共情把控", "engine": "engines_psychology", "identity_key": "reader_agent"},
        "compliance": {"name": "合规&数据校验", "engine": ["engines_logic", "story_gate"], "identity_key": "critic"},
        "devils_advocate": {"name": "魔鬼代言人", "engine": "engines_reasoning", "identity_key": "critic"},
    }

    def __init__(self, book_dir: str = ""):
        self.book_dir = book_dir
        self._logs: List[Dict] = []

    def get_agent_summary(self) -> str:
        """输出智能体分工概览（用于注入生成 prompt）"""
        lines = ["【多智能体分工体系】"]
        for key, info in self.AGENT_MAP.items():
            lines.append(f"  [{info['name']}] → {info['engine']}")
        return "\n".join(lines)

    def log_agent_call(self, agent_key: str, action: str, result: Any = None):
        """记录智能体调用日志"""
        info = self.AGENT_MAP.get(agent_key, {"name": agent_key})
        self._logs.append({
            "agent": agent_key,
            "name": info["name"],
            "action": action,
            "result": str(result)[:100] if result else "ok",
        })
        _log.debug(f"Agent [{info['name']}]: {action}")

    def get_call_log(self) -> List[Dict]:
        return self._logs[-50:]

    def get_call_log_text(self) -> str:
        """输出智能体调用日志文本（用于复盘）"""
        if not self._logs:
            return ""
        lines = ["【智能体调用日志】"]
        for log in self._logs[-20:]:
            lines.append(f"  [{log['name']}] {log['action']} -> {log['result']}")
        return "\n".join(lines)


    def get_agent_identity(self, agent_key: str) -> str:
        """获取指定智能体的 System Identity 提示词"""
        try:
            from .identity_provider import get_identity, get_prompt
            info = self.AGENT_MAP.get(agent_key)
            if info:
                ident = info.get("identity_key")
                if ident:
                    return get_identity(ident)
            return ""
        except Exception:
            return ""

    def get_all_identities_text(self) -> str:
        """获取所有智能体 System Identity 文本（用于注入 Prompt）"""
        try:
            from .identity_provider import get_identity
            parts = ["【多智能体分工与身份定义】"]
            seen = set()
            for key, info in self.AGENT_MAP.items():
                ident_key = info.get("identity_key")
                if ident_key and ident_key not in seen:
                    seen.add(ident_key)
                    ident_text = get_identity(ident_key)
                    if ident_text:
                        parts.append(f"  {ident_text}")
            return "\n".join(parts)
        except Exception:
            return self.get_agent_summary()


def create_coordinator(book_dir: str = "") -> AgentCoordinator:
    return AgentCoordinator(book_dir)
