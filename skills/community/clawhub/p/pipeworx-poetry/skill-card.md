## Description:

Poetry MCP - PoetryDB API (free, no auth).

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect an agent to a hosted PoetryDB MCP endpoint for poem search, lookup by author, and random poem retrieval without API-key setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connection instructions run an unpinned npm package from the mutable latest tag.

Mitigation: Review before installing and prefer a pinned, reviewed mcp-remote version or a preinstalled verified local executable.

Risk: The hosted MCP endpoint may receive agent requests over the network.

Mitigation: Run with minimal filesystem, environment variable, and network access appropriate to the deployment.

## Reference(s):

- [Pipeworx Poetry homepage](https://pipeworx.io/packs/poetry)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration]

**Output Format:** [Markdown and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill exposes MCP tools for poem search, poems by author, and random poems.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
