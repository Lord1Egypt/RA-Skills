# Translate a README into Simplified Chinese

English localization stub for the v2 beta bundle.
Use the Chinese source-of-truth prompt below if any wording differs during the beta rollout.

Chinese title: 把英文 README 翻译成中文写到 output.md

## Chinese source prompt

# 把 README.md 翻译成中文

工作目录下有一份英文 `README.md`（一个开源 CLI 工具的说明文档）。

请把它完整翻译成中文，输出到同目录下的 `output.md`。要求：

- 保留原 markdown 结构（标题层级、代码块、列表都不变）
- 代码块里的代码**不翻译**，但代码块上下文的描述要翻译
- 命令行参数（`--flag`）、专有名词（GitHub、API、Docker 等）保留英文
- 译文要符合中文技术文档习惯（不要硬翻"Please find the…"为"请查找……"），通顺自然
- output.md 中至少包含 3 个 markdown heading（`#` / `##` / `###`）
