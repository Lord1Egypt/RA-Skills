## Description:

通过 shell 控制 JoyCode CLI 工具进行代码生成和 AI 辅助编程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kangzhixing](https://clawhub.ai/user/kangzhixing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate JoyCode CLI from a shell for AI-assisted code generation, code review, interactive programming sessions, and automated coding tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to run a broad shell-based coding CLI with full-auto file editing and approval-policy changes.

Mitigation: Use it only in a sandboxed or version-controlled project, avoid running as root, keep approvals restrictive, and review diffs before accepting changes.

Risk: Installing an npm CLI globally can introduce supply-chain and environment-wide risk.

Mitigation: Pin and verify the package where possible before installation, and install only when JoyCode CLI is intentionally required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kangzhixing/skills/joycode)
- [Publisher profile](https://clawhub.ai/user/kangzhixing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and CLI workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent may produce code edits, review notes, command suggestions, and session-management guidance through JoyCode CLI workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
