## Description: <br>
生产缺陷分析专家，提供RCA根因分析、责任定界、相似缺陷归纳、历史查重及缺陷汇总与趋势分析功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wal1234](https://clawhub.ai/user/wal1234) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, QA engineers, and production support teams use this skill to analyze production defects, compare similar incidents, assign responsibility based on evidence, and produce structured defect summaries and trend reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production logs and historical defect records may contain secrets, personal data, or other sensitive operational details. <br>
Mitigation: Confirm that the data is appropriate to share with the agent, and redact secrets and personal data before use. <br>
Risk: RCA conclusions and responsibility assignments may be incomplete or misleading if the source evidence is partial. <br>
Mitigation: Treat generated conclusions as draft analysis and verify them against logs, tickets, code changes, and operational evidence before acting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wal1234/kaozhutiskill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown reports with headings, lists, tables, and code blocks for logs or snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include RCA narratives, defect clustering tables, responsibility analysis, deduplication comparisons, trend summaries, remediation guidance, and redacted sensitive values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
