## Description:

帮助销售人员从公开渠道整理指定区域或锚点周边的企业线索、拜访路线和定制话术。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanzy798](https://clawhub.ai/user/hanzy798)

### License/Terms of Use:

MIT-0

## Use Case:

销售人员可按区域和行业寻找潜在客户，或从指定地址规划周边企业的步行拜访；结果包含公开企业信息、潜力分级和开场话术。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ordinary user feedback can trigger persistent edits to the installed skill, bypassing review.

Mitigation: Require a separate review and approval step before changing the installed SKILL.md.

Risk: Generated CSV or XLSX cells may contain unsafe content from public sources.

Mitigation: Sanitize spreadsheet cells before opening or sharing generated files.

Risk: Lead collection can expose personal information or rely on stale public listings.

Mitigation: Use only authorized public business sources; exclude private contact details and verify source dates before outreach.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/hanzy798/skills/hyc-sales-prospector)

## Skill Output:

**Output Type(s):** [Text, Files, Guidance]

**Output Format:** [Markdown visit plan or CSV prospect roster with optional XLSX spreadsheet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source attribution, lead grades, route suggestions, and tailored outreach scripts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
