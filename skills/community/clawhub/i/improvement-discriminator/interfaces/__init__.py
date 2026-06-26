"""
Improvement Discriminator Interfaces

Critic Engine V2 + External Regression + Human Review + Assertions + LLM Judge

Note: FrozenBenchmark and HiddenTestSuite are owned by benchmark-store.
Import them directly from skills/benchmark-store/interfaces/ if needed.
"""

from .critic_engine import CriticEngineV2, CriticConfig
from .external_regression import (
    ExternalRegressionHook,
    RegressionSuiteResult,
    RegressionSourceType,
    create_regression_result,
)
from .human_review import (
    HumanReviewManager,
    HumanReviewReceipt,
    ReviewDecision,
    ReviewSeverity,
    create_review_finding,
)
from .llm_judge import (
    LLMJudge,
    JudgeConfig,
    JudgeVerdict,
)

__all__ = [
    # Critic Engine V2
    "CriticEngineV2",
    "CriticConfig",
    # External Regression
    "ExternalRegressionHook",
    "RegressionSuiteResult",
    "RegressionSourceType",
    "create_regression_result",
    # Human Review
    "HumanReviewManager",
    "HumanReviewReceipt",
    "ReviewDecision",
    "ReviewSeverity",
    "create_review_finding",
    # LLM Judge
    "LLMJudge",
    "JudgeConfig",
    "JudgeVerdict",
]
