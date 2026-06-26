"""
Step Executor - 已廢棄

此模塊原用於 LLM 自動執行，但 Booster 現已改為「思考框架」模式。

LLMBooster 不需要 LLM endpoint，LLM 自己跟隨框架思考：

1. Plan: 讀取 prompts/plan.md → 制定計劃
2. Draft: 讀取 prompts/draft.md → 撰寫初稿
3. Self-Critique: 讀取 prompts/self_critique.md → 審視問題
4. Refine: 讀取 prompts/refine.md → 優化輸出

LLM 可以：
- 自己決定使用哪個深度 (1-4)
- 自己讀取 prompt templates
- 自己執行每個步驟
- 不需要 Python 代碼調用

這就是「思考框架」的價值 —— 不是自動化，而是結構化思考。
"""

from __future__ import annotations

# 此模塊已廢棄，保留僅作文檔用途
__deprecated__ = True
__doc__ = """
使用方式：

CLI 命令：
    /booster status - 查看狀態
    /booster stats - 查看統計
    /booster depth <N> - 設定深度

LLM 執行：
    自己讀取 prompts/*.md 並跟隨框架思考
"""

# Step definitions for reference
STEP_ORDER = ["plan", "draft", "self_critique", "refine"]

STEP_DESCRIPTIONS = {
    "plan": "分析任務，制定結構化計劃",
    "draft": "根據計劃撰寫完整初稿",
    "self_critique": "審視初稿，列出改進點",
    "refine": "應用改進，優化最終輸出",
}