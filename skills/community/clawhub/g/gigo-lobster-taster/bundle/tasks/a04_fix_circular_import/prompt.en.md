# Fix the circular import

English localization stub for the v2 beta bundle.
Use the Chinese source-of-truth prompt below if any wording differs during the beta rollout.

Chinese title: 修复循环依赖导致的 ImportError

## Chinese source prompt

# 修复循环依赖导致的 ImportError

`src/user.py` 与 `src/order.py` 之间存在循环 import：

- `user.py` 在模块顶层 `from src.order import Order`
- `order.py` 在模块顶层 `from src.user import User`

跑测试时会抛 `ImportError`。请重构这两个文件以打破循环依赖（常见做法：把其中一个 import 延后到函数体内、或抽出共用的轻量类型）。

约束：保持 `User` 与 `Order` 的公共 API（构造签名、`Order.create_for(user, items)` 等）不变；不要修改 `tests/`。
