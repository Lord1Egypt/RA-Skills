"""
技能评估器 - 量化评分系统
"""

import re
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class EvaluationResult:
    """评估结果"""
    score: float
    passed: bool
    breakdown: Dict[str, float]
    details: Dict[str, Any]
    suggestions: List[str]


class SkillEvaluator:
    """
    技能评估器
    
    评分公式：
    Score = w1 * SR + w2 * Sp + w3 * R + w4 * Q
    
    - SR (Success Rate): 测试成功率
    - Sp (Speed): 速度百分比 (1 - actual_time/timeout)
    - R (Robustness): 鲁棒性得分
    - Q (Quality): 代码质量
    """
    
    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None,
        pass_threshold: float = 0.7
    ):
        self.weights = weights or {
            "success_rate": 0.4,
            "speed": 0.2,
            "robustness": 0.2,
            "quality": 0.2
        }
        self.pass_threshold = pass_threshold
    
    def evaluate(
        self,
        test_results: List,
        execution_times: List[float],
        code: str,
        timeout: int = 10
    ) -> EvaluationResult:
        """评估技能"""
        # 1. 计算成功率 (SR)
        sr = self._calculate_success_rate(test_results)
        
        # 2. 计算速度 (Sp)
        sp = self._calculate_speed(execution_times, timeout)
        
        # 3. 计算鲁棒性 (R)
        robustness = self._calculate_robustness(code)
        
        # 4. 计算代码质量 (Q)
        quality = self._calculate_quality(code)
        
        # 5. 综合评分
        score = (
            self.weights["success_rate"] * sr +
            self.weights["speed"] * sp +
            self.weights["robustness"] * robustness +
            self.weights["quality"] * quality
        )
        
        # 6. 生成建议
        suggestions = self._generate_suggestions(sr, sp, robustness, quality, test_results)
        
        return EvaluationResult(
            score=round(score, 3),
            passed=score >= self.pass_threshold,
            breakdown={
                "SR (Success Rate)": round(sr, 3),
                "Sp (Speed)": round(sp, 3),
                "R (Robustness)": round(robustness, 3),
                "Q (Quality)": round(quality, 3)
            },
            details={
                "total_tests": len(test_results),
                "passed_tests": sum(1 for r in test_results if getattr(r, 'success', False)),
                "avg_execution_time": sum(execution_times) / len(execution_times) if execution_times else 0,
                "code_lines": len(code.split('\n'))
            },
            suggestions=suggestions
        )
    
    def _calculate_success_rate(self, test_results: List) -> float:
        """计算成功率"""
        if not test_results:
            return 0.0
        passed = sum(1 for r in test_results if getattr(r, 'success', False))
        return passed / len(test_results)
    
    def _calculate_speed(self, execution_times: List[float], timeout: int) -> float:
        """计算速度得分"""
        if not execution_times:
            return 0.0
        avg_time = sum(execution_times) / len(execution_times)
        speed = max(0, 1 - avg_time / timeout)
        return speed
    
    def _calculate_robustness(self, code: str) -> float:
        """计算鲁棒性得分"""
        checks = []
        
        has_try_except = bool(re.search(r'\btry\s*:', code)) and bool(re.search(r'\bexcept\s*:', code))
        checks.append(("try-except", has_try_except))
        
        has_validate = bool(re.search(r'def\s+validate_input', code))
        checks.append(("validate_input", has_validate))
        
        has_null_check = bool(re.search(r'if\s+.*(?:is\s+not\s+None|null)', code, re.I))
        checks.append(("null_check", has_null_check))
        
        has_type_check = bool(re.search(r'isinstance\(|type\(', code))
        checks.append(("type_check", has_type_check))
        
        has_error_return = bool(re.search(r'return\s*\{[^}]*["\']success["\']\s*:\s*False', code))
        checks.append(("error_return", has_error_return))
        
        passed = sum(1 for _, p in checks if p)
        return passed / len(checks) if checks else 0.0
    
    def _calculate_quality(self, code: str) -> float:
        """计算代码质量"""
        if not code:
            return 0.0
        
        score = 0.0
        factors = []
        
        has_type_hints = bool(re.search(r':\s*(?:str|int|float|bool|dict|list|Any|Optional)', code))
        factors.append(("type_hints", has_type_hints, 0.25))
        
        has_docstring = bool(re.search(r'""".*"""', code, re.DOTALL))
        factors.append(("docstring", has_docstring, 0.25))
        
        lines = len(code.split('\n'))
        good_length = lines <= 500 and lines >= 10
        factors.append(("good_length", good_length, 0.25))
        
        error_mentions = len(re.findall(r'\b(?:error|exception|fail)\b', code, re.I))
        reasonable_errors = 1 <= error_mentions <= 10
        factors.append(("reasonable_errors", reasonable_errors, 0.25))
        
        for _, passed, weight in factors:
            if passed:
                score += weight
        
        return score
    
    def _generate_suggestions(self, sr: float, sp: float, r: float, q: float, test_results: List) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        if sr < 0.8:
            suggestions.append("测试成功率偏低，建议检查执行逻辑")
        if sp < 0.5:
            suggestions.append("执行速度偏慢，考虑优化算法")
        if r < 0.6:
            suggestions.append("鲁棒性不足，建议添加异常处理")
        if q < 0.6:
            suggestions.append("代码质量有待提升，添加类型提示")
        
        failed_cases = [r for r in test_results if not getattr(r, 'success', False)]
        if failed_cases:
            for failed in failed_cases[:3]:
                error = getattr(failed, 'error', 'Unknown error')
                suggestions.append("Case {} failed: {}".format(getattr(failed, 'case_name', 'unknown'), error))
        
        if not suggestions:
            suggestions.append("代码质量良好，无需改进")
        
        return suggestions


if __name__ == "__main__":
    from tester import TestResult, SimpleTester
    
    code = '''
class TestSkill:
    """测试技能"""
    
    def execute(self, name: str = "World") -> dict:
        if not name:
            return {"success": False, "error": "Name is required"}
        try:
            return {"success": True, "result": "Hello, {}!".format(name)}
        except Exception as e:
            return self.handle_error(e)
    
    def validate_input(self, inputs: dict) -> bool:
        return "name" in inputs
    
    def handle_error(self, error: Exception) -> dict:
        return {"success": False, "error": str(error)}
'''
    
    evaluator = SkillEvaluator()
    
    test_results = [
        TestResult("test1", True, {"result": "Hello, World!"}, None, 0.1),
        TestResult("test2", True, {"result": "Hello, Alice!"}, None, 0.15),
    ]
    
    times = [0.1, 0.15]
    
    result = evaluator.evaluate(test_results, times, code)
    
    print("\n评估结果")
    print("总分: {} ({})".format(result.score, "通过" if result.passed else "未通过"))
    print("\n详细评分:")
    for k, v in result.breakdown.items():
        print("  {}: {}".format(k, v))
    
    print("\n建议:")
    for s in result.suggestions:
        print("  - {}".format(s))
