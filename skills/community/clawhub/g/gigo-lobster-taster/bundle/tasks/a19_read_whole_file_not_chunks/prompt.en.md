# Read the whole file instead of chunking blindly

English localization stub for the v2 beta bundle.
Use the Chinese source-of-truth prompt below if any wording differs during the beta rollout.

Chinese title: 整读一个文件，不分多次分块读

## Chinese source prompt

# 概括 README

请阅读工作目录下的 `README.md`（约 500 行），然后把**不超过 3 句话**的概括写到 `summary.txt`。

**关键约束**：`Read` 工具调用总次数应 ≤ 2，且不应分块读（不要用 `offset`/`limit` 分多次读取同一文件）。该文件虽然长，但整读一次就够了。
