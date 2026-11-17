## Description:

Helps OpenClaw users invoke Claude Code CLI for code development, code review, bug fixing, tests, automation tasks, and Aliyun Bailian-compatible provider configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kotoriy](https://clawhub.ai/user/kotoriy)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to operate Claude Code from OpenClaw for implementation, review, refactoring, testing, documentation, repository workflow, and model-provider setup tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup examples can run remote PowerShell installer code if copied directly.

Mitigation: Review commands before execution and prefer WinGet or a verified installer source.

Risk: Placeholder MCP and package examples can lead users to install untrusted components.

Mitigation: Replace placeholder commands with pinned packages from trusted publishers before use.

Risk: Logs, diffs, code, or API keys may be exposed to model providers or local configuration files.

Mitigation: Avoid sending sensitive inputs to providers and store API keys with protected secret handling and least-privilege scopes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kotoriy/skills/openclaw-claude-code-bailian)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command patterns for interactive PTY usage, print mode, permissions, MCP setup, and provider environment configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
