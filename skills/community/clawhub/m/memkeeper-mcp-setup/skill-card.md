## Description:

Install, configure, verify, or remove local-first Memkeeper memory for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teflon07](https://clawhub.ai/user/teflon07)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install and register Memkeeper as a local stdio MCP server, configure local embedding and reranking, verify the MCP connection, or remove the registration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells the agent to download and run an unpinned remote installer script.

Mitigation: Review the installer source before use and prefer a pinned release or verified checksum/signature.

Risk: The skill registers a persistent local MCP memory server that stores user-level memory outside the current project by default.

Mitigation: Install only when that persistence is intended, use a separate store for project isolation when needed, and avoid printing stored memory contents or sensitive environment values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teflon07/skills/memkeeper-mcp-setup)
- [Memkeeper installer script referenced by the skill](https://raw.githubusercontent.com/teflon07/memkeeper/main/install.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local MCP setup, verification, and removal guidance; avoids reporting stored memory contents or secrets.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
