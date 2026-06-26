# 给现有模块补测试至 80% 覆盖率

`src/calc.py` 中实现了一个小工具集合（`add_positive`、`safe_div`、`grade`），目前 `tests/test_calc.py` 只测了一个 happy path。

请在 `tests/test_calc.py` **追加测试**（不要删除现有），覆盖到所有分支：

- 错误路径（除零、负数等）
- 各种 if/elif 分支

评估器会用 stdlib `trace` 模块测 `src/calc.py` 的行覆盖率，目标 ≥ 80%。
