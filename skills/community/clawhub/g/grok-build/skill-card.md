## Description:

Grok Build helps agents install, build, configure, and use xAI's terminal AI coding agent CLI/TUI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get setup and usage guidance for Grok Build, including installation commands, source build commands, project structure, and major CLI/TUI capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommended install commands execute remotely downloaded scripts without verification.

Mitigation: Prefer a versioned installer or binary from the official release channel, verify checksums or signatures when available, and inspect scripts before running them.

Risk: Grok Build is a powerful coding agent that can modify files, run shell commands, use network access, and authenticate through a browser.

Mitigation: Use it in a trusted workspace with least necessary privileges, avoid elevated permissions unless clearly required, and review proposed file and command changes.

## Reference(s):

- [ClawHub Grok Build skill page](https://clawhub.ai/chen6896qqwee/skills/grok-build)
- [xAI CLI](https://x.ai/cli)
- [xAI Build documentation](https://docs.x.ai/build/overview)
- [Grok Build GitHub repository](https://github.com/xai-org/grok-build)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include install and build commands; review commands before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
