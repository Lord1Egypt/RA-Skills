---
name: tdd
version: 1.0.0
description: 测试驱动开发 - 严格红/绿/重构循环，一次一个垂直切片，测试先行。含pytest/mock示例和覆盖率检查
tags: [testing, tdd, development, quality, refactoring]
author: laosi
source: original
---

# TDD — Test-Driven Development

> 激活词: TDD / 测试驱动 / 测试先行

## 核心循环

```
🔴 RED       → 写一个失败的测试
🟢 GREEN     → 写最少代码让测试通过
🔄 REFACTOR  → 重构，同时保持所有测试通过
```

每次迭代不超过5分钟。如果超过，说明测试范围太大了。

## Python 实现

```python
from dataclasses import dataclass, field
from typing import List, Callable

@dataclass
class TestCase:
    name: str
    fn: Callable
    passed: bool = False
    error: str = ""

class TDDCycle:
    def __init__(self):
        self.tests: List[TestCase] = []
        self.implementation: str = ""
    
    def write_test(self, name: str, test_fn: Callable) -> TestCase:
        """RED阶段: 先写测试（预期会失败）"""
        tc = TestCase(name=name, fn=test_fn)
        self.tests.append(tc)
        try:
            test_fn()
            tc.passed = True
        except AssertionError as e:
            tc.passed = False
            tc.error = f"预期失败 ✅: {e}"
        except Exception as e:
            tc.passed = False
            tc.error = f"预期失败 ✅: {e}"
        return tc
    
    def run_tests(self) -> dict:
        """GREEN阶段: 跑所有测试"""
        results = {"passed": 0, "failed": 0, "total": len(self.tests)}
        for tc in self.tests:
            try:
                tc.fn()
                tc.passed = True
                results["passed"] += 1
            except Exception as e:
                tc.passed = False
                tc.error = str(e)
                results["failed"] += 1
        return results
    
    def refactor(self, new_code: str):
        """REFACTOR阶段: 改进实现"""
        self.implementation = new_code
        results = self.run_tests()
        if results["failed"] > 0:
            raise RuntimeError(
                f"重构后 {results['failed']} 个测试失败，回滚！"
            )
        return results

# 实际TDD演示：开发一个斐波那契函数

# 🔴 STEP 1: 写测试
def fib_test_basic():
    assert fib(0) == 0
    assert fib(1) == 1

def fib_test_nth():
    assert fib(2) == 1
    assert fib(3) == 2
    assert fib(4) == 3
    assert fib(5) == 5

def fib_test_edge():
    try:
        fib(-1)
        assert False, "应该抛出异常"
    except ValueError:
        pass

def fib_test_large():
    assert fib(50) == 12586269025

# 🟢 STEP 2: 实现（先写最简单的）
def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# 运行TDD循环
cycle = TDDCycle()

print("=== 🔴 RED: 先写测试（测试应该失败）===")
for name, fn in [("basic", fib_test_basic), ("nth", fib_test_nth),
                 ("edge", fib_test_edge), ("large", fib_test_large)]:
    tc = cycle.write_test(name, fn)
    status = "✅" if tc.passed else "🔴"
    print(f"  {status} {tc.name}: {tc.error if tc.error else 'passed'}")

print("\n=== 🟢 GREEN: 实现功能（测试应该通过）===")
results = cycle.run_tests()
print(f"  通过: {results['passed']}/{results['total']}")

print("\n=== 🔄 REFACTOR: 优化代码 ===")
# 改用线性递归（虽然不如迭代，但展示了重构）
def fib_refactored(n: int, memo=None) -> int:
    if memo is None:
        memo = {0: 0, 1: 1}
    if n < 0:
        raise ValueError("n must be non-negative")
    if n not in memo:
        memo[n] = fib_refactored(n - 1, memo) + fib_refactored(n - 2, memo)
    return memo[n]

try:
    cycle.refactor("fib_refactored")
    # 重新定义函数
    import builtins
    builtins.fib = fib_refactored
    results2 = cycle.run_tests()
    print(f"  重构后: {results2['passed']}/{results2['total']} 通过 ✅")
except RuntimeError as e:
    print(f"  重构失败: {e}")
```

## pytest 集成

```python
# test_fib.py — 用pytest写TDD测试
import pytest

def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

class TestFib:
    def test_base_cases(self):
        assert fib(0) == 0
        assert fib(1) == 1
    
    def test_normal_cases(self):
        assert fib(10) == 55
        assert fib(20) == 6765
    
    def test_large_input(self):
        assert fib(100) == 354224848179261915075
    
    def test_invalid_input(self):
        with pytest.raises(ValueError):
            fib(-1)
    
    @pytest.mark.parametrize("n,expected", [
        (0, 0), (1, 1), (2, 1), (3, 2),
        (4, 3), (5, 5), (6, 8), (7, 13),
    ])
    def test_parametrized(self, n, expected):
        assert fib(n) == expected

# 命令行运行:
# pytest test_fib.py -v
# pytest test_fib.py --cov  # 配合 coverage 看行覆盖率
```

## TDD守则

| 规则 | 说明 |
|------|------|
| 测试先于实现 | 一行实现代码都不能写在测试之前 |
| 一次一个测试 | 写一个测试→让它通过→下一个 |
| 最小实现 | 写刚好让测试通过的最少代码 |
| 全绿才重构 | 有任何测试失败时，不允许重构 |
| 重构不改变行为 | 重构只改结构，不改功能 |

## 使用场景

1. **新功能开发**: 先定义接口契约（测试），再实现
2. **Bug修复**: 先写复现Bug的测试，再修代码
3. **重构遗留代码**: 先写特性测试作为安全网
4. **设计探索**: 通过测试用例探索API设计

## 依赖

- Python 3.8+
- pytest (可选，用于自动化测试运行)
