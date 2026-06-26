"""
Meta-Skill Generator - 沙盒测试系统
"""
import subprocess
import tempfile
import os
import time
import json
from pathlib import Path
from datetime import datetime

# Paths
# 获取项目根目录（相对于当前文件位置）
SKILLS_ROOT = Path(__file__).parent.parent / "skills"
SANDBOX_DIR = SKILLS_ROOT / "meta-skill-generator" / "sandbox"
SANDBOX_DIR.mkdir(parents=True, exist_ok=True)

class SimpleSandbox:
    """简化沙盒 - 在临时目录执行代码"""
    
    def __init__(self, timeout=10, memory_limit="100MB"):
        self.timeout = timeout
        self.memory_limit = memory_limit
    
    def test_code(self, code: str, test_input=None) -> dict:
        """在沙盒中测试代码"""
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # 执行代码
            start_time = time.time()
            
            if test_input:
                # 带输入执行
                result = subprocess.run(
                    ['python', temp_file],
                    input=test_input,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )
            else:
                result = subprocess.run(
                    ['python', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )
            
            execution_time = time.time() - start_time
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "execution_time": round(execution_time, 3)
            }
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Timeout",
                "execution_time": self.timeout
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "execution_time": 0
            }
        finally:
            # 清理临时文件
            try:
                os.unlink(temp_file)
            except:
                pass

def run_tests(skill_name: str, code: str, test_cases: list) -> dict:
    """运行测试用例"""
    sandbox = SimpleSandbox(timeout=10)
    
    results = []
    total_time = 0
    
    for i, test_case in enumerate(test_cases):
        test_input = test_case.get("input")
        expected = test_case.get("expected")
        
        result = sandbox.test_code(code, test_input)
        
        # 检查是否符合预期
        if expected:
            # 简化：检查输出是否包含预期字符串
            success = expected in result.get("stdout", "")
        else:
            success = result["success"]
        
        results.append({
            "case": i + 1,
            "success": success,
            "output": result.get("stdout", "")[:100],
            "error": result.get("error"),
            "time": result.get("execution_time", 0)
        })
        
        total_time += result.get("execution_time", 0)
    
    # 统计
    passed = sum(1 for r in results if r["success"])
    total = len(results)
    
    return {
        "skill_name": skill_name,
        "total_tests": total,
        "passed": passed,
        "failed": total - passed,
        "success_rate": round(passed / total, 3) if total > 0 else 0,
        "total_time": round(total_time, 3),
        "results": results
    }

# Test
if __name__ == "__main__":
    print("=== Sandbox Tester ===\n")
    
    # 测试代码
    test_code = """
import sys
data = sys.stdin.read().strip()
print(f"Hello: {data}")
"""
    
    # 测试用例
    test_cases = [
        {"input": "World", "expected": "Hello: World"},
        {"input": "Test", "expected": "Hello: Test"},
    ]
    
    # 运行测试
    result = run_tests("test_skill", test_code, test_cases)
    
    print(f"Skill: {result['skill_name']}")
    print(f"Tests: {result['passed']}/{result['total_tests']} passed")
    print(f"Success Rate: {result['success_rate']}")
    print(f"Total Time: {result['total_time']}s")
    
    print("\nDetails:")
    for r in result["results"]:
        status = "OK" if r["success"] else "FAIL"
        print(f"  Case {r['case']}: {status}")
