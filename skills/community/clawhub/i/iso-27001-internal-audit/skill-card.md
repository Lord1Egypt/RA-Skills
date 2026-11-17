## Description:

Guides an agent through ISO 27001 internal audit scoping, control assessment, evidence collection, findings generation, and corrective action recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance teams, security owners, and internal auditors use this skill to run structured ISO 27001:2022 readiness or internal audits, prioritize control testing, collect audit evidence, and draft findings with corrective actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit exports, screenshots, and interview notes may contain sensitive business, personal, or administrative information.

Mitigation: Store collected evidence only in approved encrypted locations and redact unnecessary personal or admin details before sharing.

Risk: Evidence collection commands can query production, cloud, identity, source-control, or incident-management systems.

Mitigation: Run commands only against systems the auditor is authorized to assess and avoid pasting raw exports, tokens, or secrets into unsecured chats or reports.

Risk: Procedural audit guidance can produce incomplete or misleading conclusions if scoping, sampling, or control interpretation is wrong.

Mitigation: Have a qualified compliance owner or auditor review scope, evidence, findings, and corrective actions before relying on the report.

## Reference(s):

- [Internal ISO Audit](https://internalisoaudit.com)
- [Internal ISO Audit MCP endpoint](https://internalisoaudit.com/api/mcp)
- [ClawHub skill page](https://clawhub.ai/stevenobiajulu/skills/iso-27001-internal-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON MCP configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown-only procedural guidance; optional connector support can provide live control lookup when configured.]

## Skill Version(s):

0.1.0 (source: server release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
