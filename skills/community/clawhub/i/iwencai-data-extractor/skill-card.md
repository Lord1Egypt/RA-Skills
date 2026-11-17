## Description:

从同花顺问财(iwencai.com) AI 选股页面批量抓取涨停股票数据，通过 agent-browser 连接 Chrome CDP 操作浏览器，将结果存入 SQLite 并导出 Excel 汇总报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hj2916](https://clawhub.ai/user/hj2916)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to extract iwencai limit-up stock data for selected trade dates, store it in a local SQLite database, and prepare an Excel summary for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a local Chrome debug session against iwencai.

Mitigation: Use a separate Chrome debug profile and run it only against the intended iwencai session.

Risk: The scripts create local SQLite and Excel files at configured paths.

Mitigation: Review DB_PATH and OUT_PATH before running so generated files are written to expected locations.

Risk: Scraped text in generated spreadsheets could be interpreted as formulas.

Mitigation: Treat generated spreadsheets as untrusted reports and sanitize scraped text before sharing or opening in sensitive environments.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/hj2916/skills/iwencai-data-extractor)
- [同花顺问财 AI 选股页面](https://www.iwencai.com/unifiedwh/stockpicker/)
- [爬取脚本完整参考](references/crawl_reference.md)
- [常见问题排查](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local Chrome CDP automation and local SQLite/Excel file generation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
