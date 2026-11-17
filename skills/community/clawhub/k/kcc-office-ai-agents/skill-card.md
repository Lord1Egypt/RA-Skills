## Description:

AI Agents collaboration system for KCC Office v2 that enables autonomous operation and collaboration of office agents with persistent context and self-improvement capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gasol36ai-dev](https://clawhub.ai/user/gasol36ai-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and office automation teams use this skill to initialize and operate role-specific AI agents for KCC Office v2, including coordination, persistent memory, heartbeat checks, and inter-agent collaboration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and account checks can expose private workspace, email, calendar, or social context.

Mitigation: Install in a sandboxed workspace without those credentials unless that access is intentional, and review memory promotion before preserving sensitive information.

Risk: The skill encourages instruction-file edits, self-improvement, and commits or pushes with weak user control.

Mitigation: Require explicit approval before instruction-file edits, memory promotion, commits, pushes, or other durable changes.

Risk: Shell scripts create, copy, and touch files under role-derived agent paths.

Mitigation: Validate agent role names and run scripts only from the intended workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gasol36ai-dev/skills/kcc-office-ai-agents)
- [Publisher profile](https://clawhub.ai/user/gasol36ai-dev)
- [PixiJS documentation](https://pixijs.download/release/docs/index.html)
- [Gemini API documentation](https://ai.google.dev/gemini-api/docs)
- [Web image optimization](https://web.dev/articles/image-optimization)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and workspace configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local agent workspace, memory, onboarding, status, heartbeat, and shutdown files when its scripts are run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
