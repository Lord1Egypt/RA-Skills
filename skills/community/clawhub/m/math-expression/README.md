# Math Expression Skill

使用 Wolfram Engine 处理明确的数学求解、化简、展开与数值计算请求。

## 适用场景

- 代数运算与符号化简
- 微积分：积分、求导、极限、留数
- 方程与方程组求解
- ODE/PDE 的解析解或数值解
- 级数、Taylor/Laurent、渐近展开
- 线性代数：矩阵、行列式、特征值、秩、逆矩阵
- 精确值与高精度数值计算

## 不适用场景

- 普通代码表达式求值
- shell、Python、C++、JavaScript 等编程语言运算
- API 成本、业务指标、报价之类的非数学“计算”
- 只讨论概念、不要求实际求值或化简的提问

## 快速测试

以下命令既可验证脚本功能，也可用来快速检查这个 skill 的触发边界是否仍然符合预期。

```bash
# 代数化简
python3 scripts/eval_expression.py --expr "Factor[x^4 - 1]" --json

# 定积分
python3 scripts/eval_expression.py --expr "Integrate[x^2 Exp[-x], {x, 0, Infinity}]" --json

# 极限
python3 scripts/eval_expression.py --expr "Limit[(Sin[x] - x)/x^3, x -> 0]" --json

# ODE 解析解
python3 scripts/eval_expression.py --expr "DSolve[y''[x] + y[x] == 0, y[x], x]" --json

# 渐近展开
python3 scripts/eval_expression.py --expr "Asymptotic[LogGamma[x], x -> Infinity, 5]" --json

# 矩阵特征值
python3 scripts/eval_expression.py --expr "Eigenvalues[{{1, 2}, {3, 4}}]" --json

# 高精度数值
python3 scripts/eval_expression.py --expr "N[Pi, 80]" --precision 80 --json
```

建议额外用自然语言 prompt 做一次冒烟检查：

- 应触发：“把 `x^4 - 1` 因式分解”“解这个 ODE：`y'' + y = 0`”
- 不应触发：“calculate API monthly cost”“解释一下什么是 PDE”

## 触发原则

这个 skill 会优先响应明显的数学意图，包括：

- “把 `x^4 - 1` 因式分解”
- “求 `∫_0^∞ x^2 e^{-x} dx`”
- “解这个 ODE：`y'' + y = 0`”
- “给出 `Gamma[x]` 在无穷远处的渐近展开”
- “求这个矩阵的特征值”

以下请求不应触发：

- “帮我算一下这个 bash 表达式会输出什么”
- “calculate API monthly cost”
- “这个 if 条件 `a && (b || c)` 怎么算”
- “解释一下什么是 PDE”

## 安全说明

默认情况下，脚本会阻止包含高风险 Wolfram 符号的表达式，例如：

- `Import`, `Export`, `Get`, `Put`
- `URLRead`, `URLExecute`
- `Run`, `RunProcess`, `StartProcess`

如需在隔离环境中解除限制，可使用 `--allow-unsafe`。

## 依赖

- Python 3
- `wolframclient`
- `WolframKernel`
