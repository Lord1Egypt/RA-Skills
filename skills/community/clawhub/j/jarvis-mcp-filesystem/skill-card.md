## Description:

Jarvis MCP Filesystem lets an agent use mcporter with an MCP filesystem server to read files, list directories, search by pattern, and inspect file metadata within the workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claudedamir-art](https://clawhub.ai/user/claudedamir-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give Jarvis workspace-scoped filesystem access through MCP commands for reading files, listing directories, searching files, and checking file metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad read access to the OpenClaw workspace.

Mitigation: Use it only with workspaces that do not contain secrets, credentials, or sensitive agent memory.

Risk: The documented installation uses an unpinned global npm package.

Mitigation: Prefer a pinned, locally scoped install of the MCP filesystem server where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/claudedamir-art/skills/jarvis-mcp-filesystem)
- [Publisher profile](https://clawhub.ai/user/claudedamir-art)
- [Model Context Protocol servers](https://github.com/modelcontextprotocol/servers)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter and mcp-server-filesystem; commands are intended to stay scoped to the configured workspace root.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
