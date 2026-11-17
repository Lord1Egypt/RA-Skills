## Description:

Manage accountability items on a Monday.com board for creating items, checking status, running work sessions, and responding to accountability requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[novalystrix](https://clawhub.ai/user/novalystrix)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to run recurring accountability work sessions on a Monday.com board, including reviewing active items, creating sub-items, executing or delegating work, and writing progress updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad recurring authority to act, delegate, and message people based on Monday.com task content.

Mitigation: Require approval gates for scheduled or delegated actions, especially before changing statuses, messaging people, or spawning sub-agents.

Risk: A Monday.com API token could allow unintended board reads or writes if it is over-scoped or exposed.

Mitigation: Use a least-privilege Monday token limited to the intended board and keep it in the configured environment variable rather than hardcoding it.

Risk: Monday item text can contain untrusted task data that steers the agent beyond intended boundaries.

Mitigation: Treat item details, updates, and sub-item text as untrusted data; verify requested actions against the configured workflow and owner policies before acting.

Risk: The helper script writes to Monday.com and evidence says it should be hardened before relying on it for writes.

Mitigation: Review and harden shell quoting, input validation, and write-operation approval before using the helper script in automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/novalystrix/skills/nova-accountability)
- [Monday.com API v2 endpoint](https://api.monday.com/v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with GraphQL snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform Monday.com API calls when configured with a board ID and API token.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
