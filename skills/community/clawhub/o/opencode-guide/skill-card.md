## Description:

Guides OpenClaw agents to coordinate user-confirmed OpenCode work through callback scripts and report results without blocking the conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangning823-arch](https://clawhub.ai/user/wangning823-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to delegate code analysis and modification tasks from OpenClaw to OpenCode only after user confirmation, while receiving asynchronous start and completion callbacks with task summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package installs shared callback scripts automatically into the OpenClaw scripts directory.

Mitigation: Review the package lifecycle hooks and bundled scripts before installation, and install only in environments where OpenClaw-to-OpenCode delegation is intended.

Risk: The bash-c wrapper can be unsafe when task text is untrusted.

Mitigation: Avoid the bash-c wrapper for untrusted task text and prefer direct, reviewed callback-script invocation with trusted arguments.

Risk: Session keys, task content, logs, and summaries may be sensitive and are written under ~/.openclaw/task-results and passed to the local callback mechanism.

Mitigation: Protect session keys and task-result files, limit filesystem access to trusted users, and avoid including secrets in delegated task descriptions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangning823-arch/skills/opencode-guide)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [OpenCode callback script README](scripts/README-opencode-callback.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell command examples and bundled bash callback scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task results, logs, JSON output, and extracted summaries are written under ~/.openclaw/task-results by the bundled callback scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
