# Call grep with the right arguments

English localization stub for the v2 beta bundle.
Use the Chinese source-of-truth prompt below if any wording differs during the beta rollout.

Chinese title: 工具调用参数对仗（Grep 正确 path/pattern）

## Chinese source prompt

# 在 src/ 下找出所有定义 `def main` 的文件

请用 `Grep` 工具，在工作目录的 `src/` 子目录下搜索所有定义了 `def main` 的 Python 文件。把命中的文件名（仅文件名，每行一个）写入 `answer.txt`。

**关键约束**：调用 `Grep` 时 `pattern` 必须包含 `def main`，`path` 必须设为 `src/`（或等价路径），不要漫无目的地全工作目录搜或用错关键词。
