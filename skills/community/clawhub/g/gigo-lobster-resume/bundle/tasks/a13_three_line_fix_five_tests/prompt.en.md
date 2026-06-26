# Fix five tests with a tiny patch

English localization stub for the v2 beta bundle.
Use the Chinese source-of-truth prompt below if any wording differs during the beta rollout.

Chinese title: 改 ≤3 行修 5 个失败测试

## Chinese source prompt

# 用 ≤3 行改动修复 5 个失败测试

`src/calc.py` 实现了一个加法函数 `add(a, b)`。`tests/test_calc.py` 中有 5 个测试当前全部失败。

请修改 `src/calc.py`，让所有 5 个测试通过。

**约束**：相对于初始版本，`src/calc.py` 的改动行数必须 ≤ 3 行（按 unified diff 中 `+`/`-` 行数合计统计的改动 line 数 ≤3）。优先选择最小改动方案。

不要修改 `tests/` 下的任何文件。
