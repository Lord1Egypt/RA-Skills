"""
LLMBooster - 思考框架核心

LLMBooster 是一個 4-step 思考框架，不是自動化工具。
LLM 自己跟隨框架思考，不需要 LLM endpoint。

這個模塊提供：
- 狀態管理（啟用/禁用、深度）
- 統計追蹤（tasks processed）
- CLI 命令處理

LLM 執行流程：
1. 讀取 prompts/plan.md → 制定計劃
2. 讀取 prompts/draft.md → 撰寫初稿
3. 讀取 prompts/self_critique.md → 審視問題
4. 讀取 prompts/refine.md → 優化輸出
"""

from __future__ import annotations

__version__ = "1.5.0"
__all__ = ["SkillStateManager", "CLICommandHandler", "ConfigLoader", "StreamingOutputHandler"]from state_manager import SkillStateManager
from cli_handler import CLICommandHandler
from config_loader import ConfigLoader
from stream_handler import StreamingOutputHandler

# 思考步驟順序
STEP_ORDER = ["plan", "draft", "self_critique", "refine"]

# 步驟說明
STEP_DESCRIPTIONS = {
    "plan": "分析任務，制定結構化計劃",
    "draft": "根據計劃撰寫完整初稿",
    "self_critique": "審視初稿，列出改進點",
    "refine": "應用改進，優化最終輸出",
}


def get_step_info(depth: int) -> list[dict]:
    """
    獲取指定深度的步驟信息。

    Args:
        depth: 思考深度 (1-4)

    Returns:
        步驟信息列表
    """
    steps = []
    for i, step_name in enumerate(STEP_ORDER[:depth]):
        steps.append({
            "step": i + 1,
            "total": depth,
            "name": step_name,
            "description": STEP_DESCRIPTIONS.get(step_name, ""),
        })
    return steps


def print_pipeline_start(task_preview: str = "") -> None:
    """打印 pipeline 開始信息。"""
    handler = StreamingOutputHandler()
    handler.on_pipeline_start(task_preview)


def print_step_progress(step_number: int, total_steps: int, step_name: str) -> None:
    """打印步驟進度。"""
    handler = StreamingOutputHandler()
    handler.on_step_start(step_number, total_steps, step_name)


def print_step_complete(step_name: str, time_seconds: float) -> None:
    """打印步驟完成。"""
    handler = StreamingOutputHandler()
    handler.on_step_complete(step_name, time_seconds)


def print_pipeline_complete(total_seconds: float, steps: int) -> None:
    """打印 pipeline 完成。"""
    handler = StreamingOutputHandler()
    handler.on_pipeline_complete(total_seconds, steps)