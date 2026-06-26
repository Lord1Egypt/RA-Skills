"""Data models for LLMBooster skill."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BoosterConfig:
    """LLMBooster 嘅 configuration。"""

    enabled: bool = True
    thinkingDepth: int = 4  # 1-4，決定跑幾多個 thinking step
    maxRetries: int = 3  # 1-10，每個 step 最多 retry 幾次


@dataclass
class StepResult:
    """單個 thinking step 嘅執行結果。"""

    step_name: str  # e.g. "plan", "draft", "self_critique", "refine"
    output: str  # step 嘅 LLM output
    success: bool  # 係咪成功完成
    time_taken_seconds: float  # 執行時間（秒）
    retries_used: int  # 用咗幾次 retry
    error_message: str | None  # 如果 fail，error message


@dataclass
class PipelineResult:
    """成個 pipeline 嘅執行結果。"""

    final_output: str  # 最終 output（最後成功 step 嘅 output）
    steps_executed: list[StepResult]  # 每個 step 嘅結果
    total_time_seconds: float  # 總執行時間
    completed_successfully: bool  # 所有 step 都成功
    warning_message: str | None  # 如果有 step fail，warning message


@dataclass
class CommandResult:
    """CLI command 嘅執行結果。"""

    success: bool
    message: str  # 顯示畀用戶嘅 message


@dataclass
class StatusInfo:
    """/booster status 顯示嘅資訊。"""

    enabled: bool
    thinking_depth: int
    tasks_processed: int


@dataclass
class ValidationResult:
    """Config field validation 嘅結果。"""

    valid: bool
    field_name: str
    error_message: str | None  # 如果 invalid，描述 valid range
