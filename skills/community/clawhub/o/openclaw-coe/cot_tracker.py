#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Chain of Execution (CoE)
- 实时追踪并输出OpenClaw执行过程
- 低资源消耗，只是打印执行步骤，不额外调用大模型
- 贴合 OpenClaw 实际运行流程：拆解 → 选择 → 调用 → 等待 → 结果 → 汇总
"""

from dataclasses import dataclass
from typing import List, Optional
import sys

@dataclass
class CoEStep:
    """Single step in the Chain of Execution"""
    step_type: str  # "拆解", "选择skill", "调用skill", "调用模型", "等待", "结果", "思考", "决策", "错误", "警告", "完成"
    content: str
    has_result: bool = False


class CoETracker:
    """
    Chain of Execution Tracker for OpenClaw

    Usage:
        tracker = CoETracker()
        tracker.start("分析 GTC 2026 Groq 架构")
        tracker.step("拆解问题", "把问题拆成三个部分：架构设计 / 能效对比 / 商业逻辑")
        tracker.step("选择skill", "使用 wechat-article 提取原文")
        tracker.wait() # 等待外部响应
        tracker.result("提取成功，获得 10K+ 字符原文")
        tracker.step("思考", "Groq 核心优势在确定性高带宽，命中 Agent Decoding 瓶颈")
        tracker.done("最终结论：...")
    """

    def __init__(self, enabled: bool = True, verbose: bool = True):
        self.enabled = enabled
        self.verbose = verbose
        self.steps: List[CoEStep] = []
        self._emoji_map = {
            "拆解": "🔍",
            "选择skill": "⚖️",
            "调用skill": "🔧",
            "调用模型": "🤖",
            "等待": "⏳",
            "结果": "📊",
            "思考": "🧠",
            "决策": "🤔",
            "错误": "❌",
            "警告": "⚠️",
            "完成": "✅",
            "info": "ℹ️",
        }

    def _print_step(self, emoji: str, content: str):
        """Print a step, clean line breaks for feishu"""
        if not self.enabled:
            return
        # 每个步骤单独换行，格式干净
        print(f"\n{emoji}  {content}")
        sys.stdout.flush()

    def start(self, task_title: str):
        """Start tracking a new task"""
        if not self.enabled:
            return
        self.steps.clear()
        self._print_step("🚀", f"开始处理任务：{task_title}")

    def step(self, step_type: str, content: str):
        """Add a step to the chain"""
        if not self.enabled:
            return
        emoji = self._emoji_map.get(step_type, "•")
        self.steps.append(CoEStep(step_type, content))
        self._print_step(emoji, content)

    def wait(self, content: str = "正在等待外部响应..."):
        """Indicate we're waiting for an external response (API/skill/...)"""
        self.step("等待", content)

    def result(self, content: str):
        """Report result from skill/model call"""
        self.step("结果", content)

    def error(self, content: str):
        """Report an error/status, warn user before getting stuck"""
        self.step("错误", content)

    def warn(self, content: str):
        """Warning about potential issue"""
        self.step("警告", content)

    def done(self, summary: str):
        """Complete the task and output summary"""
        if not self.enabled:
            return
        # 总结单独空一行，好看一点
        print(f"\n✅  完成\n\n{summary}")
        sys.stdout.flush()

    def is_enabled(self) -> bool:
        """Check if CoE is enabled"""
        return self.enabled

    def set_enabled(self, enabled: bool):
        """Enable/disable CoE output"""
        self.enabled = enabled

    def get_steps(self) -> List[CoEStep]:
        """Get all steps collected so far"""
        return self.steps.copy()

    def total_steps(self) -> int:
        """Get number of steps"""
        return len(self.steps)
