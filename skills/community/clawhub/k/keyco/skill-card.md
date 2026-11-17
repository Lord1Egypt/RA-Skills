## Description:

Manage Keyco assets, DUBs, workflows, lifecycle events, users, notifications, API keys, and analytics through the Keyco CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[husamabdel](https://clawhub.ai/user/husamabdel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and asset-management teams use this skill to query Keyco inventory, inspect DUB location and lifecycle state, run analytics, manage assignments and groups, and create supported lifecycle events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to run Keyco CLI commands that create, delete, revoke, clear, or change assignments and other business records.

Mitigation: Require explicit user confirmation before mutating commands and prefer read-only scopes when the task does not need write access.

Risk: The setup script can install an unpinned npm package globally and may fall back to sudo.

Mitigation: Install the Keyco CLI through a trusted non-sudo process and review the package source and version before use.

Risk: The skill uses API keys for Keyco account access.

Mitigation: Use narrowly scoped API keys, avoid exposing key values in prompts or logs, and rotate or revoke keys after automation use when appropriate.

Risk: Manual asset location or workflow-completion changes could bypass the expected audit trail.

Mitigation: Use verified scan, heartbeat, dashboard override, or lifecycle-event flows instead of attempting unsupported direct updates.

## Reference(s):

- [Full CLI command reference](references/cli-commands.md)
- [API scope reference](references/scopes.md)
- [Data integrity guidelines](references/data-integrity.md)
- [Keyco docs](https://docs.qrdub.com)
- [Keyco dashboard](https://dashboard.qrdub.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and summarized CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill prefers JSON CLI output for parsing and presents concise human-facing summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
