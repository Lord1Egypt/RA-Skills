# 案例索引

本目录主体是**免费包可跟跑或纯流程示意**的案例。免费包脚本：`sawdust_scan` / `sentence_load` / `rhythm_scan` / `doc_lint`。付费包构建时会在文末追加增补示例。

- **真实实测（含当次四检查器摘要）**：`meeting-notes-clear.md`、`device-borrow-faq.md`、`family-pension-case.md`、`terminal-readme-deai-case.md`、`skill-research-case.md`。后三篇文中若出现付费脚本结果，标为**历史摘录**；免费复现只用四检查器 + 手工改动清单。
- **流程演示**：说明如何调用规则；占位数据须替换。
- **付费练习卷**：不在本目录；随付费包 `examples/` 分发（源在开发仓 `edition/examples/`）。

| 案例 | 交付能力 | 模式 | 主要检查/交付证据 |
|---|---|---|---|
| [周会纪要写清楚](meeting-notes-clear.md) | 混乱要点→可执行纪要 | 文档写作 | 四检查器当次摘要（全 0） |
| [设备借用 FAQ](device-borrow-faq.md) | 素材→短 FAQ | 文档写作 | 四检查器当次摘要（全 0） |
| [家庭办事文档](family-pension-case.md) | 从真实材料写办事文档 | 文档写作 | 出处、模态、手工改动清单；四检查器 |
| [产品 README 去 AI 味](terminal-readme-deai-case.md) | 先诊断再保真改写 | 文章修订 | 盲读；四检查器 + 手工改动清单 |
| [同类 SKILL 调研报告](skill-research-case.md) | 从多来源材料写调研报告 | 文档写作 | 证据分级、样本表、局限单列 |
| [新写操作说明](write-sop.md) | 从素材写新文档 | 文档写作 | WRITE 五步、待核实项（未跑脚本） |
| [修订项目汇报](revise-project-report.md) | 改进既有文档并保护用户文字 | 文档修订 | 手工改动清单、范围保护 |
| [只检查，不改写](doc-checkup-only.md) | 体检并定位问题 | 文档检查 | 原句/问题/建议；四检查器口径 |
| [从研究材料写文章](article-from-research.md) | 将已确认材料组织成正文（示意） | 文章写作 | 流程示意；完整写正文见付费版 |
| [文章去 AI 味](deai-rewrite.md) | 先诊断再保真改写（占位） | 文章修订 | 流程示意；真实测见 terminal-readme-deai-case |
| 脱敏调研报告（`research-report-sample-redacted.md`） | 多来源材料→七节骨架 + 证据对账表 | 文档写作 | 流程演示；付费示例，源在 `edition/examples/`，随付费包分发 |
| PRD / 规格书（`prd-spec-sample.md`） | 必答问题→可判定验收口径 | 文档写作 | 流程演示；付费示例，源在 `edition/examples/`，随付费包分发 |
| 会议纪要可信层（`meeting-notes-trust.md`） | 行动项 + 证据与模态标注 | 文档写作 | 流程演示；付费示例，源在 `edition/examples/`，随付费包分发 |

流程演示里的「预期检查」只说明应当如何验证。真实使用时需对实际输入运行对应脚本，并报告实际结果。
