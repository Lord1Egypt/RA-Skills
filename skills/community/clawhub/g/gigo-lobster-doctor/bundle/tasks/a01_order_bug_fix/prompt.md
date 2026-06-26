# 修复订单总价计算 bug

`src/order.py` 实现了订单总价计算函数 `calculate_total(items, discount, tax_rate)`：

- `items`: list of `{"name": str, "price": float, "qty": int}`
- `discount`: 0..1 之间的折扣（0.1 表示 9 折）
- `tax_rate`: 0..1 之间的税率（0.13 表示 13%）

预期行为：`小计 = sum(price * qty)`，`折扣后 = 小计 * (1 - discount)`，`总价 = 折扣后 * (1 + tax_rate)`。

`tests/test_order.py` 中有 3 个测试。当前 `test_basic_total` 通过，`test_total_with_discount` 与 `test_total_with_tax` 失败。请修复 `src/order.py` 让所有测试通过。

注意：不要修改 `tests/` 下的任何文件。
