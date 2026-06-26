# Run five independent tasks in parallel

English localization stub for the v2 beta bundle.
Use the Chinese source-of-truth prompt below if any wording differs during the beta rollout.

Chinese title: 5 个独立任务并行执行

## Chinese source prompt

# 并行读取 5 个独立文件并汇总

工作目录下有 5 个互相独立的小文件：`file_a.txt`、`file_b.txt`、`file_c.txt`、`file_d.txt`、`file_e.txt`。

请：

1. **并行**读取这 5 个文件（在同一轮里发出多个 Read 调用，使用工具的并行能力，而非依次串行）。
2. 把每个文件的首行内容汇总到 `report.md`，每行格式：`- file_x: <首行内容>`。

**关键约束**：5 个文件的 Read 必须在同一并行批次发出（trace 中应有 ≥1 个 `parallel_group` 字段非空）。
