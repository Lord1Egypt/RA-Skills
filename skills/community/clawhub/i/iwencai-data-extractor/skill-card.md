## Description: <br>
从同花顺问财(iwencai.com) AI选股页面批量抓取涨停股票数据，使用 agent-browser 通过 Chrome CDP 连接操作浏览器，将数据存入 SQLite 数据库，并可导出为 Excel 汇总报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hj2916](https://clawhub.ai/user/hj2916) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data analysts use this skill to guide browser-based extraction of iwencai limit-up stock data for selected trading dates, store the records in SQLite, and export a multi-sheet Excel summary report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hard-coded Windows paths may point to the wrong Python, agent-browser executable, database, or output directory. <br>
Mitigation: Confirm and adjust all configured paths before running the crawl or export scripts. <br>
Risk: Chrome CDP browser automation can expose active browser state if run against an everyday profile. <br>
Mitigation: Use the documented separate Chrome debugging profile and connect only to the intended iwencai page. <br>
Risk: Automated data collection may conflict with the target site's permissions or acceptable-use rules. <br>
Mitigation: Verify that the intended scraping is allowed and use conservative request pacing. <br>
Risk: The scripts create or update local SQLite and Excel files. <br>
Mitigation: Review destination paths and back up existing data before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hj2916/iwencai-data-extractor) <br>
- [同花顺问财 AI 选股页面](https://www.iwencai.com/unifiedwh/stockpicker/) <br>
- [crawl_reference.md](references/crawl_reference.md) <br>
- [troubleshooting.md](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced workflow can create or update a local SQLite database and Excel workbook at configured paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
