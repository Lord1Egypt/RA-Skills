## Description:

Monitors Pulse inbox conversations and network requests so an agent can report new activity, urgent items, and suggested next actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xisen-w](https://clawhub.ai/user/xisen-w)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators using Pulse can use this skill to check conversations, pending network requests, and optional network context on demand or on a recurring schedule, then prioritize response actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated monitoring can expose Pulse inbox and network-request data.

Mitigation: Install only when that data access is acceptable, and use the least-privileged API key available.

Risk: Recurring cron automation can continue running and collecting activity after the user expects monitoring to stop.

Mitigation: Review any recurring-job script before scheduling it and document how to disable the cron entry.

Risk: State and log files can retain sensitive inbox or network-request activity.

Mitigation: Use private state and log directories and avoid storing unnecessary message content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xisen-w/skills/inbox-monitoring)
- [Pulse API Base URL](https://www.aicoo.io/api/v1)
- [Pulse Conversations Endpoint Example](https://www.aicoo.io/api/v1/conversations?view=all&limit=50)
- [Pulse Network Requests Endpoint](https://www.aicoo.io/api/v1/network/requests)
- [Pulse Network Context Endpoint](https://www.aicoo.io/api/v1/os/network)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PULSE_API_KEY; recurring checks may use view, limit, and state-file environment settings.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and SKILL.md metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
