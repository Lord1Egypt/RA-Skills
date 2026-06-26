# Fix the N+1 SQL query

English localization stub for the v2 beta bundle.
Use the Chinese source-of-truth prompt below if any wording differs during the beta rollout.

Chinese title: 修复 N+1 查询性能问题

## Chinese source prompt

# 修复 N+1 查询性能问题

`src/query.py` 中的 `list_users_with_order_count(conn)` 实现存在典型的 N+1 问题：

1. 先 `SELECT * FROM users` 拿到所有用户
2. 对每个用户再 `SELECT COUNT(*) FROM orders WHERE user_id = ?`

请改写为 **一次** SQL 查询（用 `LEFT JOIN ... GROUP BY` 或子查询），返回相同结构 `[{"id": int, "name": str, "order_count": int}, ...]`。

`tests/test_query.py` 会断言：

- 结果一致
- 总执行的 SQL 语句数 <= 2（理想 1）

不要修改 `tests/`。
