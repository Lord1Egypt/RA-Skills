## Description:

MemPalace provides local AI memory with semantic search, a temporal knowledge graph, and a palace-style organization model for storing and retrieving conversation context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to connect an assistant to a local memory palace for searching, browsing, and updating persistent conversation memory. It is intended for workflows where local storage and no external API keys are important.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may be read or written automatically across sessions without clear user consent.

Mitigation: Require explicit user approval before diary writes or storing new memory, and review stored memories periodically.

Risk: Mined directories or memory entries may contain secrets, personal data, or regulated information.

Mitigation: Choose mined directories carefully, exclude sensitive sources, and avoid storing secrets or regulated data.

Risk: Running the MCP server depends on the locally installed mempalace package.

Mitigation: Pin or vet the package before use and review local configuration before enabling the server.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blueworldmarketing/skills/mempalace-bwm)
- [Publisher profile](https://clawhub.ai/user/blueworldmarketing)
- [MemPalace project homepage](https://github.com/MemPalace/mempalace)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to call local MCP tools that read and write persistent memory when MemPalace is installed and configured.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
