## Description: <br>
Notion记账财务数据分析技能，自动读取支出收入流水表，全量翻页获取数据，100%解析relation类别字段，按年月类别标签多维分析并生成Markdown财务报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimislg](https://clawhub.ai/user/jimislg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Notion accounting users use this skill to fetch expense and income records, resolve relation-based categories, analyze trends by month, category, tag, and large transactions, and generate a Markdown finance report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Notion integration token and accesses private financial records. <br>
Mitigation: Use a dedicated Notion integration connected only to the required accounting data sources, and avoid pasting tokens into shared chats or shell history. <br>
Risk: The generated finance report can contain sensitive personal financial information and is written under /workspace. <br>
Mitigation: Protect access to the workspace report, review it before sharing, and delete it when no longer needed. <br>
Risk: Incorrect data_source_id values or missing Notion page connections can lead to incomplete or unintended data analysis. <br>
Mitigation: Confirm the exact expense and income data_source_id values and verify the Notion integration has access only to the intended pages before running. <br>


## Reference(s): <br>
- [Notion integrations](https://www.notion.so/my-integrations) <br>
- [ClawHub skill page](https://clawhub.ai/jimislg/notion-accounting-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with console text and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script writes a yearly finance report to /workspace/<year>_finance_report.md when run.] <br>

## Skill Version(s): <br>
1.0.5 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
