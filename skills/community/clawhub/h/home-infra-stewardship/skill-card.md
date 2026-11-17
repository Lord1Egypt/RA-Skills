## Description:

Routine NetBox, Zabbix, and homelab maintenance with responsible change authority.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gasgangrene](https://clawhub.ai/user/gasgangrene)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to perform recurring NetBox, Zabbix, and related homelab maintenance with standing authority for routine changes and approval gates for high-risk actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad standing authority to change internal infrastructure and persistent memory without tight approval boundaries.

Mitigation: Before use, define exact systems, allowed operations, approval gates for packages, permissions, scheduler jobs, sync jobs, and long-term memory updates.

Risk: Routine infrastructure changes could affect important data, public exposure, service availability, or secret handling if used outside its guardrails.

Mitigation: Require explicit human approval for destructive deletion, public or external actions, major migrations, security-policy changes, broad restarts, and any action that could expose secrets.

Risk: Maintenance work can create difficult-to-audit operational drift.

Mitigation: Keep changes small, prefer recoverable actions, create backups or snapshots before material changes when practical, verify results, and document material changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gasgangrene/skills/home-infra-stewardship)
- [Publisher profile](https://clawhub.ai/user/gasgangrene)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with command recommendations, verification notes, and maintenance documentation updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed plans for high-risk changes, rollback notes, and daily or long-term maintenance records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
