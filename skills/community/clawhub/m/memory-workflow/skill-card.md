## Description:

Memory Workflow helps agents maintain continuity by loading session memory, creating daily summaries, and prompting for important real-time memory updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rocky2046](https://clawhub.ai/user/rocky2046)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure an OpenClaw memory workflow that keeps long-term notes, daily summaries, and maintenance routines for assistant sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer adds persistent scheduled execution through cron.

Mitigation: Review the cron entry before installation and provide explicit enable, disable, and uninstall steps.

Risk: Assistant memory is stored under /root/.openclaw/workspace.

Mitigation: Use least-privilege execution and review stored memory for sensitive information before enabling the workflow.

Risk: Shell configuration handling may execute unexpected content if the config file is not trusted.

Mitigation: Parse and validate configuration values instead of sourcing the config file directly.

Risk: Installer cron editing and temporary file handling can affect unrelated cron entries or predictable paths.

Mitigation: Use a safely created temporary file and remove only the exact managed cron entry.

## Reference(s):

- [Memory Workflow ClawHub Skill Page](https://clawhub.ai/rocky2046/skills/memory-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated memory note files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates workspace memory files, templates, logs, and scheduled cron behavior when installed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
