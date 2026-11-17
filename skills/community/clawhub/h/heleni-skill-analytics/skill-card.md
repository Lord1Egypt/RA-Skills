## Description:

Tracks skill usage across agent sessions by logging invocations to a local JSONL file and generating daily summaries with top, unused, and trending skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to understand which skills are being invoked, summarize recent activity, find unused skills, and archive or reset local usage logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cross-session usage logs can include trigger phrases and context values that contain personal or group details.

Mitigation: Treat the log as sensitive, redact raw triggers and personal or group details, set restrictive file permissions, and define retention before deployment.

Risk: Echo-based JSON logging can create malformed records or unsafe shell behavior when populated with untrusted text.

Mitigation: Use a safe JSON-writing helper or serializer, validate each entry, and avoid shell interpolation for raw trigger content.

Risk: The optional cron entry creates persistent reporting behavior through a referenced local script.

Mitigation: Enable cron only after auditing the report script, documenting ownership and removal steps, and confirming the report remains local.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/heleni-skill-analytics)
- [Publisher profile](https://clawhub.ai/user/netanel-abergel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and JSONL log schema]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local JSONL log entries and daily Markdown usage summaries; optional cron scheduling is described.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
