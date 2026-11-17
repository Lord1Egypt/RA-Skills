# LGD 演化中枢 (lgd-evo) · 评测报告

> 评测口径：本技能为 meta 薄分发器，核心契约是"诚实路由 + 只读探测"。

## 评测项与结果

| # | 评测项 | 方法 | 结果 |
|---|--------|------|------|
| E1 | `--list` 列出 EVO 节点 | 运行 `--list`，核对输出节点数 = 1 | PASS |
| E2 | `--verify` 退出码纪律 | ECOSYSTEM 不报 ERROR；仅脚本异常才 rc=1 | PASS |
| E3 | 诚实分级 | 对活动工作集缺失节点返回 ECOSYSTEM 而非 LIVE | PASS |
| E4 | 只读探针 | `--verify` 仅以 `--help` 读取子技能，不做演化写/不对外写 | PASS |
| E5 | 有籍 7/7 | frontmatter 含 name/version/author/license/display_name/copyright/lineage | PASS |
| E6 | 有证 3/3 | examples/ + evidence.json + 本报告 | PASS |

## 结论

契约达成：作为薄分发器，它如实聚合并探测 EVO 阶段，未夸大、未伪绿。
