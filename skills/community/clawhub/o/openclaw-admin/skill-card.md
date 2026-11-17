## Description:

Manage and inspect the OpenClaw multi-agent gateway — list agents, check model health, view routing rules, manage crons, inspect context budgets, and run system diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atiati82](https://clawhub.ai/user/atiati82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and administer an OpenClaw multi-agent gateway, including agents, model health, routing rules, scheduled jobs, triggers, context budgets, and gateway diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes admin-context commands that can run local or registry code.

Mitigation: Install only in trusted OpenClaw workspaces, review local scripts before running full diagnostics, and prefer pinned or locally installed restart commands.

Risk: The skill may reveal local gateway configuration.

Mitigation: Treat command output as sensitive operational information and avoid sharing configuration details outside approved channels.

Risk: Routing, cron, trigger, or gateway configuration changes can alter agent behavior.

Mitigation: Require explicit approval before making configuration changes and review the affected files before applying updates.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands inspect local OpenClaw configuration and may propose administrative changes that require explicit approval.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
