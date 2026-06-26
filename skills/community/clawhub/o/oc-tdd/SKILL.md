---
name: tdd
description: Test-Driven Development assistant. Generates test cases from code or specifications, runs tests, tracks coverage, and guides the red-green-refactor cycle. Supports pytest, unittest, jest, and go test.
---

# TDD (Test-Driven Development)

测试驱动开发助手，从代码或规格生成测试用例，运行测试，追踪覆盖率，引导红-绿-重构循环。

**Version**: 1.1  
**Features**: 测试生成、测试运行、覆盖率追踪、TDD 工作流、C/C++ Unity 支持 (NEW)

---

## Quick Start

### 1. 为函数生成测试

```bash
# 为单个函数生成测试
python3 scripts/main.py generate --function "calculate_total" --file src/cart.py

# 为整个模块生成测试
python3 scripts/main.py generate --file src/cart.py --output tests/test_cart.py
```

### 2. 运行测试

```bash
# 运行所有测试
python3 scripts/main.py run

# 运行特定测试文件
python3 scripts/main.py run tests/test_cart.py

# 持续监听模式
python3 scripts/main.py run --watch
```

### 3. TDD 循环

```bash
# 开始 TDD 会话
python3 scripts/main.py cycle --file src/new_feature.py

# 检查当前状态
python3 scripts/main.py status
```

### 4. 覆盖率报告

```bash
# 生成覆盖率报告
python3 scripts/main.py coverage

# 查看未覆盖的代码
python3 scripts/main.py coverage --uncovered
```

---

## Commands

| 命令 | 说明 | 示例 |
|------|------|------|
| `generate` | 生成测试 | `generate --file src/x.py` |
| `run` | 运行测试 | `run tests/` |
| `cycle` | TDD 循环 | `cycle --file src/x.py` |
| `status` | 查看状态 | `status` |
| `coverage` | 覆盖率报告 | `coverage --html` |
| `mutant` | 变异测试 | `mutant src/` |

---

## Test Generation

### 从函数签名生成

```python
# src/calculator.py
def calculate_discount(price: float, rate: float) -> float:
    """Calculate discounted price"""
    return price * (1 - rate)
```

生成的测试：
```python
# tests/test_calculator.py
def test_calculate_discount():
    # Normal case
    assert calculate_discount(100.0, 0.2) == 80.0
    
    # Edge cases
    assert calculate_discount(0.0, 0.2) == 0.0
    assert calculate_discount(100.0, 0.0) == 100.0
    assert calculate_discount(100.0, 1.0) == 0.0
    
    # Negative tests
    with pytest.raises(ValueError):
        calculate_discount(-100.0, 0.2)
```

### 支持的测试框架

| 语言 | 框架 | 自动检测 |
|------|------|----------|
| Python | pytest | ✅ |
| Python | unittest | ✅ |
| JavaScript | Jest | ✅ |
| Go | testing | ✅ |

---

## TDD Cycle

### 红-绿-重构循环

```bash
$ python3 scripts/main.py cycle --file src/calculator.py

🔄 TDD Cycle for src/calculator.py
================================

🔴 RED: Write a failing test
   Generated: tests/test_calculator.py
   Add your test case and run: tdd run

$ # 编辑测试文件...

$ python3 scripts/main.py run
🔴 Test FAILED (expected)

💚 GREEN: Make it pass
   Implement the function to pass the test

$ # 编辑实现...

$ python3 scripts/main.py run
💚 Test PASSED

♻️  REFACTOR: Improve the code
   Run: tdd run
   Check coverage: tdd coverage

$ python3 scripts/main.py run
♻️  All tests pass, ready to refactor
```

### 状态追踪

```bash
$ python3 scripts/main.py status

📊 TDD Status
=============
Current Phase: GREEN
Last Run: 2026-04-01 18:30:00
Tests: 5 passed, 0 failed
Coverage: 87%

Next: Refactor or add new test
```

---

## Coverage

### 基本报告

```bash
python3 scripts/main.py coverage
```

输出：
```
📊 Coverage Report
==================
Total: 87%

src/calculator.py     95%  ✅
src/discount.py       72%  ⚠️
src/utils.py          45%  🔴
```

### 未覆盖代码

```bash
python3 scripts/main.py coverage --uncovered
```

输出：
```
🔍 Uncovered Lines
==================
src/discount.py:45-52  calculate_bulk_discount
src/utils.py:12-30     validate_email
```

### HTML 报告

```bash
python3 scripts/main.py coverage --html --output coverage_report/
```

---

## Configuration

`.tdd.json`:

```json
{
  "framework": "pytest",
  "test_dir": "tests",
  "source_dir": "src",
  "coverage": {
    "threshold": 80,
    "exclude": ["tests/**", "vendor/**"]
  },
  "generate": {
    "edge_cases": true,
    "error_cases": true,
    "property_tests": false
  }
}
```

---

## Examples

### 场景 1：为新功能写测试

```bash
# 1. 创建新文件
touch src/payment.py

# 2. 生成测试框架
python3 scripts/main.py generate --file src/payment.py

# 3. 编辑测试（让它失败）
# tests/test_payment.py

# 4. 运行测试（应该失败）
python3 scripts/main.py run

# 5. 实现功能（让它通过）
# src/payment.py

# 6. 运行测试（应该通过）
python3 scripts/main.py run

# 7. 重构并确保测试仍通过
python3 scripts/main.py run
```

### 场景 2：提高覆盖率

```bash
# 1. 查看当前覆盖率
python3 scripts/main.py coverage

# 2. 找到未覆盖的代码
python3 scripts/main.py coverage --uncovered

# 3. 为未覆盖的函数生成测试
python3 scripts/main.py generate --function "uncovered_func" --file src/utils.py

# 4. 再次检查覆盖率
python3 scripts/main.py coverage
```

### 场景 3：回归测试

```bash
# 修复 bug 前，先写测试
python3 scripts/main.py generate --function "buggy_function" --file src/auth.py

# 确认测试失败（复现 bug）
python3 scripts/main.py run

# 修复 bug
# ...

# 确认测试通过
python3 scripts/main.py run
```

---

## Mutation Testing

测试测试的质量：

```bash
python3 scripts/main.py mutant src/
```

原理：
1. 自动修改代码（变异）
2. 运行测试
3. 如果测试通过，说明测试不够严格

输出：
```
🧬 Mutation Testing
===================
Mutants: 45
Killed: 42 (93%) ✅
Survived: 3 (7%) ⚠️

Survived mutants:
- src/calculator.py:23  (changed + to -)
  Test didn't catch this!
```

---

## CI/CD 集成

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Tests
        run: python3 skills/tdd/scripts/main.py run
      
      - name: Coverage Check
        run: python3 skills/tdd/scripts/main.py coverage --fail-under 80
```

---

## Files

```
skills/tdd/
├── SKILL.md                    # 本文件
└── scripts/
    ├── main.py                 # ⭐ 统一入口
    ├── generator.py            # 测试生成器
    ├── runner.py               # 测试运行器
    └── coverage.py             # 覆盖率追踪
```

---

## Roadmap

- [x] 测试生成（Python）
- [x] 测试运行（pytest/unittest）
- [x] 覆盖率报告
- [ ] TDD 循环引导
- [ ] 变异测试
- [ ] JavaScript/Go 支持
- [ ] AI 辅助测试生成
