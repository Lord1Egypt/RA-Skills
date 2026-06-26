# 在 30 文件的项目里高效定位并修复 bug

工作目录是一个 30 文件的小项目。**`README.md` 已经明确指出 bug 位置：`src/parser.py` 的第 42 行附近**。

请阅读 README，按提示直接打开正确的文件，修复 bug，让 `tests/test_parser.py::test_parse_returns_int` 通过。

**关键约束**：高效完成。`Read` 工具调用总次数应 ≤ 5。不要逐个文件地翻找——README 已经给了答案位置。
