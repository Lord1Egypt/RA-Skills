---
name: math-expression
description: Use when the user wants an actual math result, simplification, expansion, exact value, high-precision value, analytic solution, or numerical solution for algebra, calculus, linear algebra, series, asymptotics, or ODE/PDE problems.
metadata:
  openclaw:
    os:
      - linux
      - darwin
      - win32
    requires:
      bins:
        - python3
        - WolframKernel
      python:
        - wolframclient
    triggers:
      patterns:
        - "(?i)\\b(simplify|fullsimplify|factor|expand|collect|reduce|substitute|eliminate|roots?)\\b|化简|因式分解|展开|配方|代换|消元"
        - "(?i)\\b(integral|integrate|derivative|differentiate|limit|residue)\\b|积分|求积分|求导|微分|极限|留数"
        - "(?i)\\b(solve|solving|equation\\s*system|nsolve|dsolve|ndsolve|ode|pde|boundary\\s*value)\\b|求解|解方程|方程组|微分方程|常微分|偏微分|边值问题"
        - "(?i)\\b(sum|series|taylor|laurent|asymptotic|asymptotics)\\b|级数|求和|泰勒|洛朗|渐近展开|渐进展开"
        - "(?i)\\b(matrix|determinant|eigenvalue|eigenvector|inverse|rank|linear\\s+algebra)\\b|矩阵|行列式|特征值|特征向量|逆矩阵|秩|线性代数"
        - "(?i)(求|解|算|化简|展开|近似|evaluate|solve|simplify|expand|factor|find)\\s*.*(∫|∂|∑|Σ|Π|lim|d/dx|partial|eigen|det|rank|x\\^|y''|->)"
        - "(?i)(∫|∂|∑|Σ|Π|lim|d/dx).*(是多少|怎么解|怎么展开|exact|numeric|solution|approximation)"
        - "(?i)\\b[Nn]\\[.*,\\s*\\d+\\]"
        - "(?i)\\b(Integrate|D|Limit|Solve|Reduce|DSolve|NDSolve|Series|Asymptotic|MatrixExp|Eigenvalues|Det)\\s*\\["
      when: |
        Use this skill when the user wants a concrete mathematical result, simplification, expansion,
        exact value, high-precision value, analytic solution, or numerical solution.

        Typical requests include algebra, calculus, limits, linear algebra, series, Taylor/Laurent
        expansions, asymptotic expansions, and ODE/PDE problems that can be expressed as a single
        Wolfram Language expression.

        Do not use this skill for ordinary code expression evaluation, shell or programming-language
        operators, API or business cost calculations, or conceptual discussion that does not ask for
        actual mathematical manipulation.
---

# Math Expression

## Overview

Use this skill when a natural-language math request should be translated into a single Wolfram Language expression and then evaluated or solved.

It fits symbolic algebra, calculus, exact arithmetic, high-precision numerics, matrix problems, series, asymptotics, and ODE/PDE tasks. It does not replace a general code executor or a multi-step notebook workflow.

## Quick start

```bash
python3 -m pip install --user wolframclient
python3 {baseDir}/scripts/eval_expression.py --expr "Factor[x^4 - 1]"
python3 {baseDir}/scripts/eval_expression.py --expr "DSolve[y''[x] + y[x] == 0, y[x], x]"
python3 {baseDir}/scripts/eval_expression.py --expr "N[Pi, 80]" --precision 80 --json
```

## Safety boundary

- Use this skill for math-only Wolfram Language expressions.
- By default, the script blocks filesystem, network, and process-related symbols such as `Import`, `URLRead`, `Run`, `RunProcess`, `Get`, `Put`, `OpenRead`, and `OpenWrite`.
- Do not disable this guard unless the runtime is isolated.
- This skill is not a general code execution tool and not a multi-step notebook agent.

## Workflow

1. Convert the user's request into one Wolfram Language expression.
2. Check that the expression is math-only.
3. Run `scripts/eval_expression.py --expr "..."`
4. Return `Exact`, `Numeric`, `Verified`, and `Version`.

## Examples

- Algebraic simplification: `Factor[x^4 - 1]`
- Definite integral: `Integrate[x^2 Exp[-x], {x, 0, Infinity}]`
- Limit: `Limit[(Sin[x] - x)/x^3, x -> 0]`
- ODE analytic solution: `DSolve[y''[x] + y[x] == 0, y[x], x]`
- PDE numeric solution: `NDSolve[{D[u[x, t], t] == D[u[x, t], {x, 2}], u[0, t] == 0, u[1, t] == 0, u[x, 0] == Sin[Pi x]}, u, {x, 0, 1}, {t, 0, 1}]`
- Asymptotic expansion: `Asymptotic[LogGamma[x], x -> Infinity, 5]`
- High-precision value: `N[Pi, 120]`

## Notes

- Input is Wolfram Language only.
- This skill is single-expression and single-run.
- Runtime dependency: `wolframclient` and `WolframKernel`.
