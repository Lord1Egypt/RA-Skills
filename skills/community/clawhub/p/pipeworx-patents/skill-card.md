## Description:

Patents MCP — wraps PatentsView API (https://api.patentsview.org/)

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and patent researchers use this skill to search patents, retrieve patent records, and search inventors through the PatentsView-backed Pipeworx MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs mcp-remote from npm with a mutable latest version at install or runtime.

Mitigation: Use a pinned, reviewed mcp-remote version or a controlled installation path before use.

Risk: Patent queries are sent through Pipeworx's gateway.

Mitigation: Avoid sending sensitive files, credentials, or private research queries unless the gateway is approved for that use.

## Reference(s):

- [Pipeworx patents pack](https://pipeworx.io/packs/patents)
- [PatentsView API](https://api.patentsview.org/)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-patents)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown or structured MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides search_patents, get_patent, and search_inventors through a remote MCP gateway.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
