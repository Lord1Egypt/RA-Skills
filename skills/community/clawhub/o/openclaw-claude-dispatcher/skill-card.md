## Description:

Dispatches long-running coding tasks to Claude Code CLI with automatic callback notifications to Feishu or WeCom when complete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xclipse](https://clawhub.ai/user/xclipse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate substantial coding tasks, project creation, feature work, refactoring, or codebase improvements to Claude Code CLI while receiving completion notifications in Feishu or WeCom.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can dispatch background coding tasks with broad permissions.

Mitigation: Prefer an approval-requiring permission mode for sensitive repositories and review resulting diffs or outputs before relying on the work.

Risk: The skill includes hard-coded Feishu and WeCom notification destinations.

Mitigation: Confirm the intended notification recipient for each dispatch and replace defaults when they do not match the user's channel.

Risk: The skill depends on local dispatcher and notification hook scripts outside the submitted artifact.

Mitigation: Install only in environments where the referenced dispatcher and notification hook are controlled and trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xclipse/skills/openclaw-claude-dispatcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dispatcher command arguments, project directory choices, notification channel details, and completion confirmation text.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
