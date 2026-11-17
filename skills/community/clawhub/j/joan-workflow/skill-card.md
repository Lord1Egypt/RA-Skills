## Description:

This skill provides workflow guidance for Joan's knowledge management system, including pods, todos, plans, workspace management, context sync, and related CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donny-son](https://clawhub.ai/user/donny-son)

### License/Terms of Use:


## Use Case:

Developers and AI-assisted development teams use this skill to understand Joan workspace concepts and choose the right Joan CLI workflow for pods, todos, plans, context generation, and workspace synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Context generation can write Joan workspace information into local context files such as CLAUDE.md.

Mitigation: Review tracked pods and generated context before using, committing, or sharing local context files.

Risk: Push and synchronization commands can share local pod, todo, or plan changes with the Joan server.

Mitigation: Confirm the intended workspace and tracked pods before running push or synchronization commands.

## Reference(s):

- [Joan MCP server](https://joan.land/mcp/joan)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; users should review local context files and tracked pods before sharing or syncing.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
