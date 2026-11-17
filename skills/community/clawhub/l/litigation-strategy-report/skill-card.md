## Description:

自动生成中国诉讼案件的《诉讼策略与类案检索报告》，基于案情拆解争议焦点并编排法条/类案检索工具，当用户提到案件分析、诉讼策略、类案检索、法条检索或庭前准备时使用本 Skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolalam](https://clawhub.ai/user/coolalam)

### License/Terms of Use:

MIT-0

## Use Case:

Lawyers and litigation teams use this skill to turn mainland China case facts into a structured litigation strategy and similar-case research report. It helps identify dispute issues, plan legal and case searches, summarize retrieved authorities, and frame evidence, procedural, settlement, and risk considerations.

### Deployment Geography for Use:

Global; substantive legal analysis is scoped to mainland China law.

## Known Risks and Mitigations:

Risk: Legal search terms may contain sensitive, personal, or privileged case facts that are sent to DeliLegal.

Mitigation: Redact personal and privileged facts before search and use the skill only when external legal API disclosure is acceptable.

Risk: The scripts disable TLS certificate verification while sending an API key and case details.

Mitigation: Restore TLS certificate verification before real use and verify the endpoint certificate chain.

Risk: The API key is read from a project-local config file.

Mitigation: Prefer an environment variable or managed secret store and avoid committing populated config files.

Risk: Generated litigation guidance or retrieved legal material may be incomplete, outdated, or misapplied to the user's facts.

Mitigation: Have a qualified reviewer verify current official legal texts, case relevance, and assumptions before relying on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolalam/skills/litigation-strategy-report)
- [Search query patterns](references/search-query-patterns.md)
- [DeliLegal API key management](https://open.delilegal.com/personal/keys)
- [DeliLegal law search API endpoint](https://platform.delilegal.com/api/v1/generice/law/list)
- [DeliLegal case search API endpoint](https://platform.delilegal.com/api/v1/generice/case/list)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with inline shell commands and legal search result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured DeliLegal API key before executing searches; legal conclusions are conditional on the user's facts and retrieved authorities.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
