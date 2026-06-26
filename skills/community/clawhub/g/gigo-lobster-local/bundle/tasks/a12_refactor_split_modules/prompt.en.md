# Refactor one large file into modules

English localization stub for the v2 beta bundle.
Use the Chinese source-of-truth prompt below if any wording differs during the beta rollout.

Chinese title: 把单文件拆成 3 个模块

## Chinese source prompt

# 把单文件 src/app.py 拆成 3 个模块

`src/app.py` 是一个 200 行的"全家桶"：里面同时包含 `User`、`Order`、`Invoice` 三块逻辑。请重构为：

- `src/users.py`：放 `User` 与相关函数
- `src/orders.py`：放 `Order` 与相关函数
- `src/invoices.py`：放 `Invoice` 与相关函数

约束：

- 每个新模块行数 ≤ 80 行
- `src/app.py` 必须删除或缩减为只 re-export（行数 ≤ 20）
- `tests/test_app.py` 中的 import 应改为从拆分后的模块 import（测试文件已经写成 `from src.users import User`、`from src.orders import Order`、`from src.invoices import Invoice` 的形式，不要改测试）。
- 所有现有测试通过
