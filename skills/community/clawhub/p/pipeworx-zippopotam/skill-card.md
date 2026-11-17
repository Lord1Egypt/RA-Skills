## Description:

ZIP and postal code lookup - get place names, states, and coordinates for postal codes in 60+ countries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up postal or ZIP code details, validate address fields, populate city and state data, and find postal codes for cities across supported countries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup queries are sent to Pipeworx.

Mitigation: Use the skill only when sending postal lookup inputs to Pipeworx is acceptable for the intended workflow.

Risk: The MCP configuration runs mcp-remote from npm using a mutable latest version.

Mitigation: Pin mcp-remote to a reviewed version or install it through a controlled dependency process before use.

## Reference(s):

- [Pipeworx Zippopotam homepage](https://pipeworx.io/packs/zippopotam)
- [Pipeworx Zippopotam MCP endpoint](https://gateway.pipeworx.io/zippopotam/mcp)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [JSON lookup results with Markdown examples for shell commands and MCP configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup requests are sent to the Pipeworx MCP endpoint; example local setup uses mcp-remote from npm.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
