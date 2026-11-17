## Description:

Create, debug, and maintain OpenClaw Gateway internal hooks for agent bootstrap events, virtual context injection, notification workflows, and hook troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cbd2020](https://clawhub.ai/user/cbd2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build and troubleshoot OpenClaw Gateway internal hooks that run during agent lifecycle events. It is especially suited for bootstrap-file injection, hook registration, logging, and Telegram or webhook notification debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example hooks can inject virtual bootstrap files and change future agent context.

Mitigation: Review every bootstrapFiles change before enabling a hook and keep injected content narrow to the intended workflow.

Risk: Notification examples may read OpenClaw configuration to obtain bot tokens or other sensitive values.

Mitigation: Replace placeholders and prefer explicit environment variables or scoped secrets over reading the full OpenClaw config.

Risk: Broad always-on hooks may run during more sessions than intended.

Mitigation: Scope hook conditions to specific event types, actions, sessions, and workspaces before deployment.

## Reference(s):

- [Complete hook example](references/complete-example.js)
- [OpenClaw Hook Development release page](https://clawhub.ai/cbd2020/skills/openclaw-hook)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes example hook patterns and placeholder values that should be reviewed before use.]

## Skill Version(s):

1.0.2 (source: server release metadata, created 2026-03-14T14:01:46Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
