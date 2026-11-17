## Description:

Huo15 Plan Mode helps an agent identify risky shell operations, pause before execution, request user confirmation, and record confirmation activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a confirmation checkpoint around commands that may delete data, change system state, push Git history, install dependencies, or make network calls. It is intended to support human review before potentially destructive agent actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The integration helper can execute arbitrary shell commands without protection when Plan Mode is disabled or when a command is classified as not dangerous.

Mitigation: Do not source or use the integration wrapper until it fails closed by default, avoids eval-based execution, and requires confirmation for unknown or risky commands.

Risk: Setup modifies persistent OpenClaw workspace files and writes command activity logs.

Mitigation: Review the setup script before installation, confirm the intended HEARTBEAT.md changes, and monitor or rotate logs under ~/.openclaw/workspace/memory/activity.

Risk: The security scan verdict is suspicious because the skill is protective in intent but has unsafe execution behavior.

Mitigation: Review this skill carefully before installing and treat it as untrusted until the execution wrapper and confirmation behavior are hardened.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell-oriented command guidance with JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write confirmation logs under ~/.openclaw/workspace/memory/activity and update ~/.openclaw/workspace/HEARTBEAT.md during setup.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact version text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
