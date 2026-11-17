## Description:

Pokemon MCP - wraps PokeAPI (free, no auth required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to a Pokemon-focused MCP server that exposes Pokemon, type, ability, and evolution-chain lookup tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connection recipe uses an npm helper fetched dynamically with mcp-remote@latest, which can introduce supply-chain drift.

Mitigation: Pin mcp-remote to a reviewed version and run the MCP process with least-privilege environment access before deployment.

## Reference(s):

- [Pipeworx Pokemon Pack](https://pipeworx.io/packs/pokemon)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-pokemon)
- [Publisher profile](https://clawhub.ai/user/brucegutman)

## Skill Output:

**Output Type(s):** [Configuration, Shell commands, Guidance]

**Output Format:** [Markdown with JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MCP connection guidance for a remote Pokemon tool server.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
