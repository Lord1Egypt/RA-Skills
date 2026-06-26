"""
技能优化器 - 双轨优化策略
"""

import json
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class OptimizationStrategy(Enum):
    """优化策略"""
    REWRITE = "改写法"
    COMPRESS = "压缩法"


@dataclass
class OptimizationResult:
    """优化结果"""
    strategy: OptimizationStrategy
    code: str
    score: float
    changes: List[str]
    passed: bool


class SkillOptimizer:
    """
    技能优化器
    
    双轨策略：
    1. 改写法：保留原逻辑，修复所有错误
    2. 压缩法：简化逻辑，保持功能
    """
    
    def __init__(self, llm_client=None, model: str = "deepseek/deepseek-coder"):
        self.llm_client = llm_client
        self.model = model
    
    def optimize(
        self,
        original_code: str,
        error: str,
        expected_output: Optional[str] = None,
        test_cases: Optional[List[Dict]] = None
    ) -> Tuple[OptimizationResult, OptimizationResult]:
        """优化技能代码"""
        if not self.llm_client:
            return self._optimize_local(original_code, error)
        
        try:
            return self._optimize_with_llm(original_code, error, expected_output)
        except Exception as e:
            print("LLM 优化失败: {}，使用本地优化".format(e))
            return self._optimize_local(original_code, error)
    
    def _optimize_with_llm(self, original_code: str, error: str, expected_output: Optional[str]) -> Tuple[OptimizationResult, OptimizationResult]:
        """使用 LLM 优化"""
        prompt = """你是一个技能优化器。根据错误信息，优化技能代码。

原始代码：
{}
错误信息：
{}
期望输出：
{}

请提供两个版本的优化代码：
版本A（改写法）：保留原逻辑，修复错误
版本B（压缩法）：简化代码，保持功能

输出JSON格式：
{{"version_a": {{"code": "...", "changes": [...]}}, "version_b": {{"code": "...", "changes": [...]}}}}""".format(
            original_code, error, expected_output or "N/A"
        )
        
        try:
            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个技能优化专家。"},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.5
            )
            
            result = json.loads(response.choices[0].message.content)
            
            version_a = OptimizationResult(
                strategy=OptimizationStrategy.REWRITE,
                code=result.get("version_a", {}).get("code", original_code),
                score=0.0,
                changes=result.get("version_a", {}).get("changes", []),
                passed=False
            )
            
            version_b = OptimizationResult(
                strategy=OptimizationStrategy.COMPRESS,
                code=result.get("version_b", {}).get("code", original_code),
                score=0.0,
                changes=result.get("version_b", {}).get("changes", []),
                passed=False
            )
            
            return version_a, version_b
            
        except Exception as e:
            return self._optimize_local(original_code, error)
    
    def _optimize_local(self, original_code: str, error: str) -> Tuple[OptimizationResult, OptimizationResult]:
        """本地优化"""
        # 版本 A：改写法 - 添加基本错误处理
        rewrite_code = self._rewrite_fix_common_errors(original_code, error)
        
        # 版本 B：压缩法 - 简化代码
        compress_code = self._compress_simplify(original_code)
        
        version_a = OptimizationResult(
            strategy=OptimizationStrategy.REWRITE,
            code=rewrite_code,
            score=0.0,
            changes=["修复常见错误"],
            passed=False
        )
        
        version_b = OptimizationResult(
            strategy=OptimizationStrategy.COMPRESS,
            code=compress_code,
            score=0.0,
            changes=["简化代码结构"],
            passed=False
        )
        
        return version_a, version_b
    
    def _rewrite_fix_common_errors(self, code: str, error: str) -> str:
        """改写法：修复常见错误"""
        lines = code.split('\n')
        new_lines = []
        error_lower = error.lower()
        
        for line in lines:
            new_line = line
            
            if 'nameerror' in error_lower and 'except' not in line:
                pass
            
            if 'indentationerror' in error_lower:
                new_line = line.replace('\t', '    ')
            
            new_lines.append(new_line)
        
        if 'def execute' in code:
            if 'try:' not in code:
                execute_idx = None
                for i, line in enumerate(lines):
                    if 'def execute' in line:
                        execute_idx = i
                        break
                
                if execute_idx:
                    body_start = execute_idx + 1
                    while body_start < len(lines) and not lines[body_start].strip():
                        body_start += 1
                    
                    if body_start < len(lines):
                        indent = len(lines[body_start]) - len(lines[body_start].lstrip())
                        indent_str = ' ' * indent
                        
                        new_lines = (
                            lines[:body_start] +
                            ["{}try:".format(indent_str)] +
                            ["{}    {}".format(indent_str, lines[body_start].strip())] +
                            ["{}except Exception as e:".format(indent_str)] +
                            ["{}    return self.handle_error(e)".format(indent_str)] +
                            lines[body_start+1:]
                        )
        
        return '\n'.join(new_lines)
    
    def _compress_simplify(self, code: str) -> str:
        """压缩法：简化代码"""
        lines = code.split('\n')
        new_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            if stripped and not stripped.startswith('#'):
                new_lines.append(line)
            elif stripped.startswith('"""') or stripped.startswith("'''"):
                new_lines.append(line)
        
        compressed = []
        prev_empty = False
        
        for line in new_lines:
            is_empty = not line.strip()
            
            if is_empty and prev_empty:
                continue
            
            compressed.append(line)
            prev_empty = is_empty
        
        return '\n'.join(compressed)
    
    def optimize_with_retry(
        self,
        original_code: str,
        error: str,
        evaluator,
        test_cases: List,
        max_iterations: int = 3
    ) -> Optional[OptimizationResult]:
        """带重试的优化"""
        from tester import SimpleTester, TestCase
        
        current_code = original_code
        best_result = None
        best_score = 0.0
        
        tester = SimpleTester()
        
        for iteration in range(max_iterations):
            print("\n优化迭代 {}/{}".format(iteration + 1, max_iterations))
            
            version_a, version_b = self.optimize(current_code, error)
            
            test_cases_obj = [
                TestCase(tc.get('name', 'test{}'.format(i)), tc.get('inputs', {}), tc.get('expected', ''))
                for i, tc in enumerate(test_cases or [])
            ]
            
            results_a = tester.test_skill(version_a.code, test_cases_obj)
            times_a = [r.execution_time for r in results_a]
            eval_a = evaluator.evaluate(results_a, times_a, version_a.code)
            version_a.score = eval_a.score
            version_a.passed = eval_a.passed
            
            results_b = tester.test_skill(version_b.code, test_cases_obj)
            times_b = [r.execution_time for r in results_b]
            eval_b = evaluator.evaluate(results_b, times_b, version_b.code)
            version_b.score = eval_b.score
            version_b.passed = eval_b.passed
            
            print("  版本A: {} ({})".format(eval_a.score, "通过" if eval_a.passed else "未通过"))
            print("  版本B: {} ({})".format(eval_b.score, "通过" if eval_b.passed else "未通过"))
            
            if version_a.score >= version_b.score:
                best_result = version_a
            else:
                best_result = version_b
            
            if best_result.score > best_score:
                best_score = best_result.score
            
            if best_result.passed:
                print("优化成功！得分: {}".format(best_result.score))
                return best_result
            
            current_code = best_result.code
            error = "优化后仍未通过所有测试"
        
        print("达到最大迭代次数 {}，最佳得分: {}".format(max_iterations, best_score))
        return best_result


def create_optimizer(llm_client=None) -> SkillOptimizer:
    """创建优化器实例"""
    return SkillOptimizer(llm_client)


if __name__ == "__main__":
    code = '''
class TestSkill:
    def execute(self, name):
        return {"success": True, "result": "Hello " + name}
'''
    
    error = "TypeError: unsupported operand type(s) for +: 'str' and 'NoneType'"
    
    optimizer = SkillOptimizer()
    
    version_a, version_b = optimizer._optimize_local(code, error)
    
    print("版本 A（改写法）:")
    print(version_a.code[:500])
    
    print("\n版本 B（压缩法）:")
    print(version_b.code[:500])
