## Description:

Use the oo CLI to read Excalidraw MCP guidance and create diagrams through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can use this skill to create Excalidraw diagrams and retrieve drawing guidance through an OOMOL-connected Excalidraw MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup uses remote installer scripts, and the CLI release and backend were not independently verified.

Mitigation: Review and approve CLI installation separately using a specific verified release.

Risk: Startup skill synchronization may install additional agent skills, and diagram content is shared through OOMOL.

Mitigation: Check which additional skills will be installed, use OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization when appropriate, and share only intended diagram content through OOMOL.

## Reference(s):

- [Excalidraw MCP skill page](https://clawhub.ai/oomol/skills/oo-excalidraw-mcp)
- [oo CLI documentation](https://github.com/oomol-lab/oo-cli)
- [Excalidraw MCP API documentation](https://github.com/excalidraw/excalidraw-mcp)
- [Excalidraw](https://excalidraw.com)
- [oo CLI environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
