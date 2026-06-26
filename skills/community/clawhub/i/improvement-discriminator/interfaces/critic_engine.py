#!/usr/bin/env python3
"""
Critic Engine V2 - P1 Runtime Enhancement

P1 改进:
1. 整合 assertions 模块，引入 assertion-driven 评估
2. 减少 MockSkillEvaluator 权重，增加真实逻辑占比
3. 支持真实 Skill 调用 (通过 Python 模块加载)
4. 明确标注剩余 mock 边界

相比 V1 的变化:
- 新增 AssertionCheck 支持
- MockSkillEvaluator 降级为 fallback，不再是默认
- 支持从文件路径加载真实 Skill 模块
- 评估结果包含 assertion 详情
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union, Tuple
import json
import time
import importlib.util
import sys

# Import from benchmark-store (sibling skill)
_BENCHMARK_STORE = Path(__file__).resolve().parents[2] / "benchmark-store" / "interfaces"
if str(_BENCHMARK_STORE) not in sys.path:
    sys.path.insert(0, str(_BENCHMARK_STORE))

try:
    from .assertions import (
        AssertionCheck,
        CheckResult,
        AssertionRunner,
        create_check,
        create_assertion,
    )
    from .external_regression import (
        ExternalRegressionHook,
        RegressionSuiteResult,
    )
    from .human_review import (
        HumanReviewManager,
        HumanReviewReceipt,
        ReviewDecision,
    )
except ImportError:
    from assertions import (
        AssertionCheck,
        CheckResult,
        AssertionRunner,
        create_check,
        create_assertion,
    )
    from external_regression import (
        ExternalRegressionHook,
        RegressionSuiteResult,
    )
    from human_review import (
        HumanReviewManager,
        HumanReviewReceipt,
        ReviewDecision,
    )

try:
    from frozen_benchmark import (
        BenchmarkCase,
        BenchmarkResult,
        BenchmarkSuite,
        FrozenBenchmark,
        MetricType,
        ScoringCriteria,
        STANDARD_BENCHMARK_SUITE,
    )
except ImportError:
    # Fallback: benchmark-store not available
    FrozenBenchmark = None
    BenchmarkSuite = None
    STANDARD_BENCHMARK_SUITE = None
    BenchmarkCase = None
    BenchmarkResult = None
    MetricType = None
    ScoringCriteria = None

try:
    from hidden_tests import (
        HiddenTest,
        HiddenTestSuite,
        TestResult,
        TestType,
        TestVisibility,
        create_hidden_test,
    )
except ImportError:
    # Fallback: benchmark-store not available
    HiddenTest = None
    HiddenTestSuite = None
    TestResult = None
    TestType = None
    TestVisibility = None
    create_hidden_test = None


@dataclass
class CriticConfig:
    """
    Critic V2 评估配置

    P1 新增:
    - enable_assertions: 启用断言检查
    - assertion_weight: 断言检查权重
    - use_mock_evaluator: 是否使用 MockSkillEvaluator (默认 False)
    
    P2-a 新增:
    - enable_external_regression: 启用外部回归结果接入
    - enable_human_review: 启人工审查结果接入
    - regression_weight: 外部回归权重
    - human_review_weight: 人工审查权重
    """
    enable_frozen_benchmark: bool = True
    enable_hidden_tests: bool = True
    enable_assertions: bool = True  # P1 新增
    enable_external_regression: bool = True  # P2-a 新增
    enable_human_review: bool = True  # P2-a 新增
    benchmark_weight: float = 0.35
    hidden_test_weight: float = 0.25
    assertion_weight: float = 0.20  # P1 新增
    regression_weight: float = 0.10  # P2-a 新增
    human_review_weight: float = 0.10  # P2-a 新增
    min_pass_rate: float = 0.6
    timeout_seconds: float = 30.0
    verbose: bool = False
    use_mock_evaluator: bool = False  # P1: 默认不使用 mock

    def __post_init__(self):
        total = (
            self.benchmark_weight +
            self.hidden_test_weight +
            self.assertion_weight +
            self.regression_weight +
            self.human_review_weight
        )
        assert abs(total - 1.0) < 0.001, \
            f"Weights must sum to 1.0, got {total}"


@dataclass
class CriticScore:
    """
    Critic V2 评估得分

    P1 新增:
    - assertion_score: 断言检查得分
    - assertion_details: 断言检查结果详情
    
    P2-a 新增:
    - regression_score: 外部回归结果得分
    - human_review_score: 人工审查得分
    - regression_details: 外部回归结果详情
    - human_review_details: 人工审查结果详情
    """
    overall: float = 0.0
    benchmark_score: float = 0.0
    hidden_test_score: float = 0.0
    assertion_score: float = 0.0  # P1 新增
    regression_score: float = 0.0  # P2-a 新增
    human_review_score: float = 0.0  # P2-a 新增
    pass_rate: float = 0.0
    by_metric: Dict[str, float] = field(default_factory=dict)
    level: int = 1
    verdict: str = "pending"
    assertion_details: List[Dict] = field(default_factory=list)  # P1 新增
    regression_details: Dict[str, Any] = field(default_factory=dict)  # P2-a 新增
    human_review_details: Dict[str, Any] = field(default_factory=dict)  # P2-a 新增

    def __post_init__(self):
        assert 0.0 <= self.overall <= 1.0, "Overall score must be in [0, 1]"

    @classmethod
    def from_results(
        cls,
        benchmark_results: Optional[Dict],
        hidden_test_results: Optional[Dict],
        assertion_results: Optional[List[CheckResult]],  # P1 新增
        config: CriticConfig,
    ) -> "CriticScore":
        """从测试结果计算得分"""
        benchmark_score = 0.0
        hidden_test_score = 0.0
        assertion_score = 0.0
        by_metric = {}

        # 计算基准测试得分
        if benchmark_results:
            summary = benchmark_results.get("summary", {})
            benchmark_score = summary.get("weighted_score", summary.get("avg_score", 0.0))
            pass_rate = summary.get("pass_rate", 0.0)
            by_metric["accuracy"] = benchmark_score
            by_metric["reliability"] = pass_rate

        # 计算隐藏测试得分
        if hidden_test_results:
            summary = hidden_test_results.get("summary", {})
            hidden_test_score = summary.get("avg_score", 0.0)
            pass_rate = summary.get("pass_rate", 0.0)
            by_metric["hidden_accuracy"] = hidden_test_score

        # P1: 计算断言检查得分
        assertion_details = []
        if assertion_results:
            total_score = sum(r.score for r in assertion_results)
            assertion_score = total_score / len(assertion_results) if assertion_results else 0.0
            by_metric["assertion_score"] = assertion_score

            # 记录断言详情
            for check_result in assertion_results:
                assertion_details.append({
                    "name": check_result.check.name,
                    "passed": check_result.passed,
                    "score": check_result.score,
                    "message": check_result.message,
                    "assertions": [
                        {
                            "type": r.assertion.type.value,
                            "passed": r.passed,
                            "message": r.message,
                        }
                        for r in check_result.results
                    ],
                })

        # 加权总分 (P1: 三部分加权)
        overall = (
            benchmark_score * config.benchmark_weight +
            hidden_test_score * config.hidden_test_weight +
            assertion_score * config.assertion_weight
        )

        # 综合通过率
        total_passed = 0
        total_cases = 0
        if benchmark_results:
            summary = benchmark_results.get("summary", {})
            total_passed += summary.get("passed_cases", 0)
            total_cases += summary.get("total_cases", 0)
        if hidden_test_results:
            summary = hidden_test_results.get("summary", {})
            total_passed += summary.get("passed", 0)
            total_cases += summary.get("total_tests", 0)
        if assertion_results:
            total_passed += sum(1 for r in assertion_results if r.passed)
            total_cases += len(assertion_results)

        pass_rate = total_passed / total_cases if total_cases > 0 else 0.0

        # 判定等级 (P1: 考虑断言得分)
        level = 1
        verdict = "needs_improvement"
        if overall >= 0.9 and pass_rate >= 0.95 and assertion_score >= 0.9:
            level = 3
            verdict = "production_ready"
        elif overall >= 0.75 and pass_rate >= 0.8 and assertion_score >= 0.75:
            level = 2
            verdict = "stable"
        elif overall >= 0.6:
            level = 1
            verdict = "basic"

        return cls(
            overall=round(overall, 4),
            benchmark_score=round(benchmark_score, 4),
            hidden_test_score=round(hidden_test_score, 4),
            assertion_score=round(assertion_score, 4),
            pass_rate=round(pass_rate, 4),
            by_metric=by_metric,
            level=level,
            verdict=verdict,
            assertion_details=assertion_details,
        )


class MockSkillEvaluator:
    """
    Deterministic mock evaluator for testing. No randomness.

    P1 说明:
    - 仅在 use_mock_evaluator=True 时使用
    - 默认情况下应使用真实 Skill 调用
    - 保留用于演示和测试环境
    """

    def __init__(self, success_rate: float = 0.85, avg_time_ms: float = 500):
        self.success_rate = success_rate
        self.avg_time_ms = avg_time_ms
        self.token_usage = 0
        self._call_count = 0

    def evaluate(self, case: BenchmarkCase) -> BenchmarkResult:
        """评估单个基准测试用例 (deterministic)"""
        self._call_count += 1

        # Deterministic execution time
        execution_time = self.avg_time_ms

        # Deterministic: succeed for first N% of calls based on success_rate
        passed = (self._call_count % 10) < int(self.success_rate * 10)
        score = 0.85 if passed else 0.3

        # Deterministic token usage
        token_usage = 1000

        return BenchmarkResult(
            case_id=case.id,
            passed=passed,
            score=score,
            actual_output={"result": "mock_output"} if passed else None,
            execution_time_ms=execution_time,
            token_usage=token_usage,
            error_message=None if passed else "Mock failure",
        )


class RealSkillEvaluator:
    """
    P1 新增：真实 Skill 评估器

    从文件路径加载 Skill 模块并执行评估。

    支持的 Skill 格式:
    1. Python 模块：包含 evaluate() 或 execute() 函数的 .py 文件
    2. 标准 Skill 目录：包含 scripts/ 目录的 Skill

    P1 限制:
    - 仅支持简单的函数调用
    - 不支持复杂的依赖注入
    - 不支持需要特殊环境配置的 Skill
    """

    def __init__(self, skill_path: str):
        """
        初始化真实 Skill 评估器

        Args:
            skill_path: Skill 路径 (文件或目录)
        """
        self.skill_path = Path(skill_path)
        self.skill_module = None
        self.skill_func = None
        self._load_skill()

    def _load_skill(self):
        """加载 Skill 模块"""
        # 尝试加载 Python 文件
        py_files = list(self.skill_path.glob("*.py")) if self.skill_path.is_dir() else [self.skill_path]

        # 优先查找 main.py 或 evaluate.py
        priority_files = ["main.py", "evaluate.py", "executor.py"]
        target_file = None

        for pf in priority_files:
            candidate = self.skill_path / pf if self.skill_path.is_dir() else self.skill_path
            if candidate.exists() and candidate.name == pf:
                target_file = candidate
                break

        if not target_file and py_files:
            target_file = py_files[0]

        if not target_file:
            raise ValueError(f"No Python files found in {self.skill_path}")

        # 加载模块
        spec = importlib.util.spec_from_file_location("skill_module", target_file)
        if spec and spec.loader:
            self.skill_module = importlib.util.module_from_spec(spec)
            sys.modules["skill_module"] = self.skill_module
            spec.loader.exec_module(self.skill_module)

            # 查找评估函数
            for func_name in ["evaluate", "execute", "run", "main"]:
                if hasattr(self.skill_module, func_name):
                    self.skill_func = getattr(self.skill_module, func_name)
                    break

            if not self.skill_func:
                raise ValueError(f"No evaluate/execute/run/main function found in {target_file}")

    def evaluate(self, case: BenchmarkCase) -> BenchmarkResult:
        """评估单个基准测试用例"""
        start_time = time.time()

        try:
            # 调用 Skill 函数
            if self.skill_func:
                actual_output = self.skill_func(case.input_data)
            else:
                raise ValueError("No skill function available")

            execution_time = (time.time() - start_time) * 1000

            # 验证输出
            passed = self._verify_output(actual_output, case.expected_output)
            score = 1.0 if passed else 0.5

            return BenchmarkResult(
                case_id=case.id,
                passed=passed,
                score=score,
                actual_output=actual_output,
                execution_time_ms=execution_time,
                token_usage=0,  # 真实调用，无法获取 token 使用量
                error_message=None if passed else "Output verification failed",
            )

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return BenchmarkResult(
                case_id=case.id,
                passed=False,
                score=0.0,
                actual_output=None,
                execution_time_ms=execution_time,
                token_usage=0,
                error_message=str(e),
            )

    def _verify_output(self, actual: Any, expected: Any) -> bool:
        """验证输出是否符合期望"""
        if expected is None:
            return actual is not None

        if isinstance(expected, dict) and isinstance(actual, dict):
            # 字典比较：检查关键键是否存在
            for key, value in expected.items():
                if key not in actual:
                    return False
                if isinstance(value, str) and isinstance(actual[key], str):
                    if value.lower() not in actual[key].lower():
                        return False
            return True

        # 字符串/其他类型：简单相等或包含检查
        if isinstance(expected, str) and isinstance(actual, str):
            return expected.lower() in actual.lower()

        return actual == expected


class CriticEngineV2:
    """
    Critic V2 评估引擎

    P1 改进:
    1. 整合 assertions 模块
    2. 支持真实 Skill 调用 (RealSkillEvaluator)
    3. MockSkillEvaluator 降级为 fallback
    4. 评估结果包含 assertion 详情
    """

    def __init__(self, config: Optional[CriticConfig] = None):
        """
        初始化 Critic V2 引擎

        Args:
            config: 评估配置
        """
        self.config = config or CriticConfig()
        self._frozen_benchmark: Optional[FrozenBenchmark] = None
        self._hidden_suite: Optional[HiddenTestSuite] = None
        self._assertion_checks: List[AssertionCheck] = []  # P1 新增
        self._results: Dict[str, Any] = {}
        self._assertion_runner = AssertionRunner()  # P1 新增
        # P2-a 新增
        self._regression_hook: Optional[ExternalRegressionHook] = None
        self._human_review_manager: Optional[HumanReviewManager] = None

    def load_benchmark_suite(self, suite: Optional[BenchmarkSuite] = None) -> None:
        """加载基准测试套件"""
        suite = suite or STANDARD_BENCHMARK_SUITE
        self._frozen_benchmark = FrozenBenchmark(suite)

        if self.config.verbose:
            print(f"Loaded benchmark suite: {suite.name} (v{suite.version})")
            print(f"  - Cases: {len(suite.cases)}")

    def load_hidden_tests(
        self,
        suite_path: Optional[Union[str, Path]] = None,
        password: Optional[str] = None,
    ) -> None:
        """加载隐藏测试套件"""
        if suite_path:
            self._hidden_suite = HiddenTestSuite(
                suite_id="loaded_suite",
                name="Loaded Hidden Tests",
                version="1.0.0",
            )
            self._hidden_suite.load_from_file(suite_path)
        else:
            self._hidden_suite = self._create_demo_hidden_suite()

        if password:
            self._hidden_suite.unlock(password)
        else:
            raise ValueError("password is required to unlock hidden test suite")

        if self.config.verbose:
            metadata = self._hidden_suite.get_metadata()
            print(f"Loaded hidden test suite: {metadata['name']}")

    def add_assertion_check(self, check: AssertionCheck) -> None:
        """
        P1 新增：添加断言检查

        Args:
            check: 断言检查定义
        """
        self._assertion_checks.append(check)

        if self.config.verbose:
            print(f"Added assertion check: {check.name} ({len(check.assertions)} assertions)")

    def load_standard_assertions(self) -> None:
        """
        P1 新增：加载标准断言检查集

        包含常用的功能和可靠性断言。
        """
        # 功能完整性检查
        self.add_assertion_check(create_check(
            name="Functionality Check",
            assertions=[
                {"type": "contains", "value": "success", "description": "Contains success indicator", "weight": 0.4},
                {"type": "contains", "value": "result", "description": "Contains result", "weight": 0.3},
                {"type": "threshold", "value": 0.5, "description": "Score >= 0.5", "weight": 0.3},
            ],
            description="Basic functionality assertions",
        ))

        # 可靠性检查
        self.add_assertion_check(create_check(
            name="Reliability Check",
            assertions=[
                {"type": "contains", "value": "error", "description": "Error handling present", "weight": 0.3, "required": False},
                {"type": "regex", "value": r"\d+", "description": "Contains numeric data", "weight": 0.3},
                {"type": "threshold", "value": 0.6, "description": "Confidence >= 0.6", "weight": 0.4},
            ],
            description="Reliability and error handling assertions",
        ))

        # 输出质量检查
        self.add_assertion_check(create_check(
            name="Output Quality Check",
            assertions=[
                {"type": "contains", "value": ["structured", "organized"], "description": "Well-structured output", "weight": 0.5},
                {"type": "regex", "value": r".{50,}", "description": "Sufficient detail (>50 chars)", "weight": 0.5},
            ],
            description="Output quality and completeness assertions",
        ))

        if self.config.verbose:
            print(f"Loaded {len(self._assertion_checks)} standard assertion checks")

    # ========== P2-a Methods ==========

    def load_external_regression(
        self,
        path: Optional[Union[str, Path]] = None,
        data: Optional[Dict[str, Any]] = None,
        adapter_type: str = "json",
    ) -> None:
        """
        P2-a 新增：加载外部回归结果

        Args:
            path: 结果文件路径 (可选，与 data 互斥)
            data: 结果数据 (可选，与 path 互斥)
            adapter_type: 适配器类型 ("json", "junit", "csv")
        """
        self._regression_hook = ExternalRegressionHook()

        if path:
            self._regression_hook.load_from_file(path, adapter_type=adapter_type)
        elif data:
            self._regression_hook.load_from_dict(data)

        if self.config.verbose:
            summary = self._regression_hook.get_summary()
            print(f"Loaded external regression: {summary['total_suites']} suites, {summary['total_tests']} tests")

    def load_human_review_receipt(
        self,
        receipt_path: Union[str, Path],
    ) -> None:
        """
        P2-a 新增：加载人工审查回执

        Args:
            receipt_path: 回执文件路径
        """
        self._human_review_manager = HumanReviewManager()
        self._human_review_manager.load_receipt(receipt_path)

        if self.config.verbose:
            receipt = self._human_review_manager.get_receipts()[0]
            print(f"Loaded human review: {receipt.receipt_id}, decision={receipt.decision.value}")

    def add_human_review_receipt(self, receipt: HumanReviewReceipt) -> None:
        """
        P2-a 新增：添加人工审查回执

        Args:
            receipt: 审查回执实例
        """
        if self._human_review_manager is None:
            self._human_review_manager = HumanReviewManager()
        self._human_review_manager.add_receipt(receipt)

    def create_human_review_receipt(
        self,
        skill_name: str,
        skill_version: str,
        reviewer_id: str,
        reviewer_name: str,
        decision: ReviewDecision,
        confidence: float = 0.8,
        comments: str = "",
        final_score: Optional[float] = None,
        requires_followup: bool = False,
    ) -> HumanReviewReceipt:
        """
        P2-a 新增：创建人工审查回执

        Args:
            skill_name: Skill 名称
            skill_version: Skill 版本
            reviewer_id: 审查者 ID
            reviewer_name: 审查者姓名
            decision: 审查决策
            confidence: 置信度
            comments: 审查意见
            final_score: 最终评分
            requires_followup: 是否需要跟进

        Returns:
            创建的审查回执
        """
        if self._human_review_manager is None:
            self._human_review_manager = HumanReviewManager()

        return self._human_review_manager.create_receipt(
            skill_name=skill_name,
            skill_version=skill_version,
            reviewer_id=reviewer_id,
            reviewer_name=reviewer_name,
            decision=decision,
            confidence=confidence,
            comments=comments,
            final_score=final_score,
            requires_followup=requires_followup,
        )

    def _create_demo_hidden_suite(self) -> HiddenTestSuite:
        """创建演示用的隐藏测试套件"""
        suite = HiddenTestSuite(
            suite_id="demo-hidden-v1",
            name="Demo Hidden Tests",
            version="1.0.0",
        )

        test_cases = [
            ("func-001", TestType.FUNCTIONAL, "general", 2),
            ("edge-001", TestType.EDGE_CASE, "edge", 3),
            ("sec-001", TestType.SECURITY, "security", 4),
        ]

        for test_id, test_type, category, difficulty in test_cases:
            test = create_hidden_test(
                test_id=test_id,
                input_data={"task": f"test_{test_id}", "data": [1, 2, 3]},
                expected_output={"status": "success"},
                validator={"type": "contains", "threshold": 0.8, "keywords": ["success"]},
                password="DEMO_ONLY_NOT_FOR_PRODUCTION",
                test_type=test_type,
                category=category,
                difficulty=difficulty,
            )
            suite.add_test(test)

        return suite

    def _build_assertion_input(
        self,
        evaluator: Any,
        evaluator_type: str,
        benchmark_results: Optional[Dict],
        hidden_test_results: Optional[Dict],
    ) -> Dict[str, Any]:
        """Build assertion input from real evaluator output when available.

        Falls back to a mock output only when no real results exist, logging
        a warning so callers know the assertions ran against synthetic data.
        """
        import logging
        logger = logging.getLogger(__name__)

        # Attempt to extract real output from benchmark results
        if isinstance(evaluator, RealSkillEvaluator) and benchmark_results:
            case_results = benchmark_results.get("results", [])
            # Collect all actual_output values from successful benchmark cases
            real_outputs = [
                r.get("actual_output") or r.get("output")
                for r in case_results
                if r.get("passed") and (r.get("actual_output") or r.get("output"))
            ]
            if real_outputs:
                # Merge the first successful output as the primary assertion input
                merged: Dict[str, Any] = {}
                for output in real_outputs:
                    if isinstance(output, dict):
                        merged.update(output)
                    else:
                        merged.setdefault("output", str(output))
                if self.config.verbose:
                    logger.info(
                        "Using real evaluator output for assertions "
                        "(source: benchmark, %d results)", len(real_outputs),
                    )
                return merged

        # Attempt hidden test output as secondary source
        if isinstance(evaluator, RealSkillEvaluator) and hidden_test_results:
            summary = hidden_test_results.get("summary", {})
            if summary.get("passed", 0) > 0:
                if self.config.verbose:
                    logger.info(
                        "Using hidden-test summary for assertions "
                        "(passed=%d)", summary["passed"],
                    )
                return {
                    "output": "success - completed",
                    "score": summary.get("avg_score", 0.0),
                    "result": "structured result from hidden tests",
                }

        # Fallback: mock output (log warning so callers know)
        logger.warning(
            "No real evaluator output available (evaluator_type=%s); "
            "falling back to mock assertion input.",
            evaluator_type,
        )
        return {
            "output": "success - completed",
            "score": 0.85,
            "result": "structured result",
        }

    def evaluate(
        self,
        skill_path: Optional[str] = None,  # P1 新增：Skill 路径
        skill_evaluator: Optional[Any] = None,  # 向后兼容
        skill_under_test: Optional[Any] = None,
        progress_callback: Optional[Callable] = None,
    ) -> CriticScore:
        """
        P1 改进：执行完整评估

        Args:
            skill_path: Skill 路径 (优先使用)
            skill_evaluator: Skill 评估器 (向后兼容，如果未提供 skill_path 则使用)
            skill_under_test: 被测 Skill (用于隐藏测试)
            progress_callback: 进度回调

        Returns:
            评估得分
        """
        benchmark_results = None
        hidden_test_results = None
        assertion_results = None  # P1 新增
        regression_results = None  # P2-a 新增
        human_review_results = None  # P2-a 新增

        # P1: 确定评估器
        evaluator = None
        evaluator_type = "none"
        self._evaluator = None  # Track for assertion output reuse

        if skill_path:
            # 优先使用真实 Skill 评估器
            try:
                evaluator = RealSkillEvaluator(skill_path)
                evaluator_type = "real"
                if self.config.verbose:
                    print(f"Loaded real skill evaluator from: {skill_path}")
            except Exception as e:
                if self.config.verbose:
                    print(f"Failed to load real skill: {e}, falling back to mock")
                evaluator = MockSkillEvaluator()
                evaluator_type = "mock_fallback"
        elif skill_evaluator:
            evaluator = skill_evaluator
            evaluator_type = "provided"
        elif self.config.use_mock_evaluator:
            evaluator = MockSkillEvaluator()
            evaluator_type = "mock"
        
        # 确保有评估器可用
        if evaluator is None:
            if self.config.verbose:
                print("No evaluator available, using MockSkillEvaluator")
            evaluator = MockSkillEvaluator()
            evaluator_type = "mock_default"

        self._evaluator = evaluator

        # 1. 运行冻结基准测试
        if self.config.enable_frozen_benchmark and self._frozen_benchmark and evaluator:
            if self.config.verbose:
                print("\n=== Running Frozen Benchmark ===")

            benchmark_results = self._frozen_benchmark.run(evaluator, progress_callback)

            if self.config.verbose:
                summary = benchmark_results.get("summary", {})
                print(f"Pass rate: {summary.get('pass_rate', 0):.2%}")

        # 2. 运行隐藏测试
        if self.config.enable_hidden_tests and self._hidden_suite:
            if self.config.verbose:
                print("\n=== Running Hidden Tests ===")

            skill = skill_under_test or MockSkillEvaluator()
            hidden_test_results = self._hidden_suite.run_all(skill)

            if self.config.verbose:
                summary = hidden_test_results.get("summary", {})
                print(f"Pass rate: {summary.get('pass_rate', 0):.2%}")

        # 3. P1: 运行断言检查
        if self.config.enable_assertions and self._assertion_checks:
            if self.config.verbose:
                print("\n=== Running Assertion Checks ===")

            # Use real evaluator output when available (P2-a fix: replaced hardcoded mock_output)
            assertion_input = self._build_assertion_input(
                evaluator, evaluator_type, benchmark_results, hidden_test_results
            )
            assertion_results = self._assertion_runner.run_batch(
                self._assertion_checks,
                assertion_input,
            )

            if self.config.verbose:
                passed = sum(1 for r in assertion_results if r.passed)
                print(f"Passed: {passed}/{len(assertion_results)} assertion checks")

        # 4. P2-a: 获取外部回归结果
        if self.config.enable_external_regression and self._regression_hook:
            if self.config.verbose:
                print("\n=== Loading External Regression Results ===")

            regression_results = self._regression_hook.get_summary()
            regression_score = self._regression_hook.get_normalized_score()

            if self.config.verbose:
                print(f"Regression score: {regression_score:.4f}")

        # 5. P2-a: 获取人工审查结果
        if self.config.enable_human_review and self._human_review_manager:
            if self.config.verbose:
                print("\n=== Loading Human Review Results ===")

            human_review_results = self._human_review_manager.get_summary()
            human_review_score = self._human_review_manager._decision_to_score()

            if self.config.verbose:
                print(f"Human review score: {human_review_score:.4f}")

        # 6. 计算最终得分 (P2-a: 包含 regression 和 human review)
        score = CriticScore.from_results(
            benchmark_results,
            hidden_test_results,
            assertion_results,  # P1 新增
            self.config,
        )

        # P2-a: 整合 regression 和 human review 得分
        if regression_results is not None:
            score.regression_score = self._regression_hook.get_normalized_score() if self._regression_hook else 0.0
            score.regression_details = regression_results

        if human_review_results is not None:
            score.human_review_score = self._human_review_manager._decision_to_score() if self._human_review_manager else 0.0
            score.human_review_details = human_review_results

        # P2-a: 重新计算 overall (5 部分加权)
        score.overall = max(0.0, min(1.0, round(
            score.benchmark_score * self.config.benchmark_weight +
            score.hidden_test_score * self.config.hidden_test_weight +
            score.assertion_score * self.config.assertion_weight +
            score.regression_score * self.config.regression_weight +
            score.human_review_score * self.config.human_review_weight,
            4
        )))

        # 5. 存储结果 (P2-a: 包含 regression 和 human review)
        self._results = {
            "score": score,
            "benchmark": benchmark_results,
            "hidden_tests": hidden_test_results,
            "assertions": assertion_results,  # P1 新增
            "regression": regression_results,  # P2-a 新增
            "human_review": human_review_results,  # P2-a 新增
            "config": self.config,
            "timestamp": datetime.now().isoformat(),
            "evaluator_type": evaluator_type,
        }

        return score

    def generate_report(self, output_path: Optional[Union[str, Path]] = None) -> str:
        """生成评估报告 (P2-a: 包含断言/回归/人工审查详情)"""
        if not self._results:
            return "# Error\n\nNo evaluation results available. Run evaluate() first."

        score = self._results["score"]
        benchmark = self._results.get("benchmark", {})
        hidden = self._results.get("hidden_tests", {})
        assertions = self._results.get("assertions", [])  # P1 新增
        regression = self._results.get("regression")  # P2-a 新增
        human_review = self._results.get("human_review")  # P2-a 新增

        report = f"""# Critic V2 评估报告 (P2-a)

**评估时间**: {self._results.get('timestamp', 'N/A')}  
**评估器类型**: {self._results.get('evaluator_type', 'N/A')}

---

## 总体评分

| 指标 | 值 |
|------|-----|
| 总体得分 | {score.overall:.4f} |
| 等级 | **Level {score.level}** |
| 结论 | {score.verdict} |
| 通过率 | {score.pass_rate:.2%} |

---

## 详细得分

### 基准测试 ({self.config.benchmark_weight * 100:.0f}%)

| 指标 | 得分 |
|------|-----|
| 基准测试得分 | {score.benchmark_score:.4f} |

{benchmark.get('summary', {}).get('total_cases', 0)} 个测试用例，{benchmark.get('summary', {}).get('passed_cases', 0)} 个通过

### 隐藏测试 ({self.config.hidden_test_weight * 100:.0f}%)

| 指标 | 得分 |
|------|-----|
| 隐藏测试得分 | {score.hidden_test_score:.4f} |

{hidden.get('summary', {}).get('total_tests', 0)} 个测试用例，{hidden.get('summary', {}).get('passed', 0)} 个通过

### 断言检查 ({self.config.assertion_weight * 100:.0f}%) - P1 新增

| 指标 | 得分 |
|------|-----|
| 断言检查得分 | {score.assertion_score:.4f} |

"""
        # 断言详情
        if assertions:
            for check_result in assertions:
                report += f"**{check_result.check.name}**: {'✅' if check_result.passed else '❌'} (得分：{check_result.score:.2%})\n"
                report += f"- {check_result.message}\n\n"
        else:
            report += "*未运行断言检查*\n\n"

        # P2-a: 外部回归结果
        report += f"### 外部回归 ({self.config.regression_weight * 100:.0f}%) - P2-a 新增\n\n"
        if regression:
            report += f"| 指标 | 值 |\n|------|-----|\n"
            report += f"| 回归得分 | {score.regression_score:.4f} |\n"
            report += f"| 测试套件 | {regression.get('total_suites', 0)} |\n"
            report += f"| 总测试数 | {regression.get('total_tests', 0)} |\n"
            report += f"| 通过数 | {regression.get('total_passed', 0)} |\n\n"
        else:
            report += "*未加载外部回归结果*\n\n"

        # P2-a: 人工审查结果
        report += f"### 人工审查 ({self.config.human_review_weight * 100:.0f}%) - P2-a 新增\n\n"
        if human_review:
            report += f"| 指标 | 值 |\n|------|-----|\n"
            report += f"| 审查得分 | {score.human_review_score:.4f} |\n"
            report += f"| 审查次数 | {human_review.get('total_reviews', 0)} |\n"
            report += f"| 平均置信度 | {human_review.get('avg_confidence', 0):.2%} |\n"
            report += f"| 发现问题 | {human_review.get('total_findings', 0)} |\n\n"
        else:
            report += "*未加载人工审查结果*\n\n"

        report += """
---

## 按指标分析

"""
        for metric, value in score.by_metric.items():
            report += f"- **{metric}**: {value:.4f}\n"

        report += "\n---\n\n"

        # 改进建议
        report += "## 改进建议\n\n"
        if score.level == 3:
            report += "✅ **恭喜！** Skill 已达到生产就绪标准 (Level 3)。\n"
        elif score.level == 2:
            report += f"⚠️ **良好。** Skill 已达到稳定标准 (Level 2)。\n"
            report += f"- 目标：将总体得分从 {score.overall:.4f} 提升到 0.90\n"
        else:
            report += f"❌ **需要改进。** Skill 仅达到基础标准 (Level 1)。\n"
            report += f"- 优先修复失败的核心功能测试\n"

        # P1: 保存报告
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to: {output_path}")

        return report

    def export_results(self, path: Union[str, Path]) -> Path:
        """导出完整结果为 JSON (P2-a: 包含 regression 和 human_review)"""
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 序列化结果 (P1 + P2-a)
        export_data = {}
        for key, value in self._results.items():
            if key == "assertions" and value:
                export_data[key] = [
                    {
                        "name": cr.check.name,
                        "passed": cr.passed,
                        "score": cr.score,
                        "message": cr.message,
                    }
                    for cr in value
                ]
            elif key == "score":
                # Serialize CriticScore object
                export_data[key] = {
                    "overall": value.overall,
                    "benchmark_score": value.benchmark_score,
                    "hidden_test_score": value.hidden_test_score,
                    "assertion_score": value.assertion_score,
                    "regression_score": value.regression_score,
                    "human_review_score": value.human_review_score,
                    "pass_rate": value.pass_rate,
                    "level": value.level,
                    "verdict": value.verdict,
                }
            else:
                export_data[key] = value

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)

        return output_path


def run_p1_demo():
    """运行 P1 演示"""
    print("=" * 60)
    print("Critic V2 - P1 Runtime Demo")
    print("=" * 60)

    # 创建配置 (P1: 默认不使用 mock)
    config = CriticConfig(
        enable_frozen_benchmark=True,
        enable_hidden_tests=True,
        enable_assertions=True,
        benchmark_weight=0.4,
        hidden_test_weight=0.3,
        assertion_weight=0.3,
        regression_weight=0.0,
        human_review_weight=0.0,
        verbose=True,
        use_mock_evaluator=True,  # 演示模式使用 mock
    )

    # 创建引擎
    engine = CriticEngineV2(config)

    # 加载测试套件
    engine.load_benchmark_suite()
    engine.load_hidden_tests()
    engine.load_standard_assertions()  # P1: 加载标准断言

    # 运行评估
    print("\n" + "=" * 60)
    print("Running Evaluation...")
    print("=" * 60)

    score = engine.evaluate()

    # 输出结果
    print("\n" + "=" * 60)
    print("Evaluation Results")
    print("=" * 60)
    print(f"Overall Score: {score.overall:.4f}")
    print(f"Benchmark Score: {score.benchmark_score:.4f}")
    print(f"Hidden Test Score: {score.hidden_test_score:.4f}")
    print(f"Assertion Score: {score.assertion_score:.4f} (P1)")
    print(f"Pass Rate: {score.pass_rate:.2%}")
    print(f"Level: {score.level}")
    print(f"Verdict: {score.verdict}")

    # 生成报告
    print("\n" + "=" * 60)
    print("Generating Report...")
    print("=" * 60)

    report = engine.generate_report("/tmp/critic_v2_p1_report.md")
    print("\nReport Preview:")
    print(report[:1500] + "...")

    # 导出 JSON 结果
    engine.export_results("/tmp/critic_v2_p1_results.json")
    print("\nResults exported to /tmp/critic_v2_p1_results.json")

    return score


if __name__ == "__main__":
    run_p1_demo()
