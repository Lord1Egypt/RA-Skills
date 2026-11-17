## Description:

Zero-config OpenClaw gateway monitoring that runs health checks, sends daily summaries, alerts on critical issues, and offers approved fixes in the current channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukeaustin13](https://clawhub.ai/user/lukeaustin13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor an OpenClaw gateway, cron jobs, plugins, sessions, disk usage, and memory usage from an agent conversation. It is intended to provide concise status summaries, immediate critical alerts, and proposed operational fixes that require approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect gateway state, sessions, cron jobs, plugins, and host resource usage.

Mitigation: Install it only where OpenClaw operational monitoring is desired and review reported status before acting on recommendations.

Risk: Proposed fixes may restart services, retry cron jobs, reinstall plugins, or delete old logs.

Mitigation: Require explicit user approval, show the exact command and risk before execution, and verify the result after any approved action.

Risk: Critical alerts and scheduled summaries are sent in the active channel.

Mitigation: Use the skill only in appropriate operational channels and review scheduled summary behavior before enabling recurring reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lukeaustin13/skills/operator-dashboard)
- [Publisher profile](https://clawhub.ai/user/lukeaustin13)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Concise Markdown status summaries, alerts, detailed reports, and proposed shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the active conversation channel for replies and asks for approval before destructive or service-changing actions.]

## Skill Version(s):

1.0.0 (source: frontmatter, clawhub.json, _meta.json, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
