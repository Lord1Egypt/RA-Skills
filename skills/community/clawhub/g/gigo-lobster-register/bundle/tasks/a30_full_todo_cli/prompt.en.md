# Build the full todo CLI

English localization stub for the v2 beta bundle.
Use the Chinese source-of-truth prompt below if any wording differs during the beta rollout.

Chinese title: 完整 todo CLI

## Chinese source prompt

# 实现一个完整的 todo CLI

请在工作目录根下创建 `todo.py`，实现一个用 `argparse` 的命令行 todo 工具。要求：

## 子命令

- `python todo.py add "<text>"` — 新增一条待办，输出 `Added #<id>: <text>`
- `python todo.py list` — 列出所有待办，每行格式 `#<id> [ ] <text>`，已完成的为 `[x]`
- `python todo.py done <id>` — 标记完成，输出 `Done #<id>`
- `python todo.py delete <id>` — 删除，输出 `Deleted #<id>`

## 持久化

- 所有数据保存到当前工作目录下的 `todos.json`，重启后仍可读出。
- ID 单调递增，删除后不重用。

## 测试

测试在 `tests/test_todo.py`，请确保全部通过。不要修改测试。
