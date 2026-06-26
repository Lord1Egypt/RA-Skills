# Add type hints

English localization stub for the v2 beta bundle.
Use the Chinese source-of-truth prompt below if any wording differs during the beta rollout.

Chinese title: 给函数补类型注解并通过 mypy

## Chinese source prompt

# 给函数补类型注解并通过 mypy

`src/calc.py` 中有三个函数（`add`、`concat`、`average`）都没有类型注解。请：

1. 为每个函数的参数与返回值添加合适的类型注解（使用 `int / float / str / list[str]` 等）。
2. 保证现有 `tests/test_calc.py` 全部通过。
3. 通过 `mypy --strict src/calc.py`（若 mypy 未安装则跳过该校验）。

不要修改 `tests/`。
