## Description:

使用已在 OpenClaw 本机连接的 MedGroup MCP，查询 DRG/DIP 城市与规则、检索 ICD 编码、执行分组和结算测算、查询 CC/MCC。适用于医保分组、编码与规则核对；结果用于专业辅助。

This skill is ready for commercial/non-commercial use.

## Publisher:

[u201013903](https://clawhub.ai/user/u201013903)

### License/Terms of Use:

MIT-0

## Use Case:

External users working with Chinese medical insurance DRG/DIP workflows use this skill to query supported cities and rules, look up ICD codes, run grouping checks, estimate settlement scenarios, and review CC/MCC status. Results are intended as professional reference for coding and rule review, not final clinical, coding, audit, or reimbursement authority.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may include identifiable patient or case data while preparing grouping or settlement queries.

Mitigation: Use synthetic or de-identified case data where possible, and do not ask for or repeat patient names, ID numbers, contact details, hospitalization numbers, or similar identifiers.

Risk: MedGroup credentials could be exposed if users paste API keys into chat or commit them to skill files.

Mitigation: Keep the MedGroup key only in local MCP settings, direct users to rotate or recreate keys through MedGroup when authentication fails, and never request the key in conversation.

Risk: Grouping, coding, rule, or settlement outputs could be mistaken for final clinical, audit, or reimbursement decisions.

Mitigation: Label settlement outputs as parameter-based scenario estimates and present all tool results as professional reference that must be checked against official rules and expert review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/u201013903/skills/medgroup-drgdip-skill)
- [MedGroup homepage](https://medgroup.medchat.fun)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tool-call summaries and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the user's locally configured MedGroup MCP connection; grouping and settlement outputs should be treated as professional reference.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
