## Description:

Implements structured usage logging and audit trails for cost and session tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add session-aware JSONL usage logs, audit trails, cost tracking, and basic usage analytics to agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local usage logs can retain sensitive metadata if secrets or personal data are recorded.

Mitigation: Avoid putting secrets or sensitive personal data in log metadata, and periodically review or delete files under ~/.claude/leyline/usage.

Risk: Shared session IDs can make cross-service activity easier to correlate.

Mitigation: Use shared session IDs only when cross-service correlation is intended and appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-usage-logging)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)
- [Session Patterns](modules/session-patterns.md)
- [Log Formats](modules/log-formats.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, Python, YAML, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local logging patterns for JSONL records, session IDs, query snippets, and integration guidance.]

## Skill Version(s):

1.9.19 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
