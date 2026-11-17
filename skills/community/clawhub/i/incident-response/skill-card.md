## Description:

Structured incident response for OpenClaw system failures using a seven-phase loop from triage and evidence collection through root cause analysis, restore, prevention, monitoring, and documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunhualiao](https://clawhub.ai/user/chunhualiao)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw operators and developers use this skill to investigate system regressions, gather evidence, restore known-good configuration, add prevention measures, and set temporary monitoring after an incident.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can lead an agent to read session histories, restore configuration, restart services, change permissions, commit changes, create cron jobs, or write persistent learning files.

Mitigation: Use only with trusted OpenClaw operators and require explicit confirmation before each operational or persistent action.

Risk: Incident investigation can expose sensitive session-log evidence or affect the wrong environment if the scope is vague.

Mitigation: Scope each run to a named host and incident, redact session-log evidence, and keep monitoring jobs read-only by default.

Risk: Broad commits or open-ended monitoring can introduce unrelated changes or persistent follow-up beyond the incident.

Mitigation: Avoid git add -A, commit only reviewed prevention changes, and give monitoring jobs a fixed expiry.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chunhualiao/skills/incident-response)
- [README](README.md)
- [Quick Diagnosis Checklists](references/checklists.md)
- [Cron Job Template for Incident Monitoring](references/cron-template.md)
- [Prevention Patterns](references/prevention-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and evidence-backed incident notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include root cause chains, restore verification, prevention commits, monitoring schedules, and learning entries.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, skill.yml, CHANGELOG, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
