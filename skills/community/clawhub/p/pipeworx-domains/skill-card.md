## Description:

Search registered domain names by keyword and TLD to find what is already taken via Domainsdb.info.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and brand researchers use this skill to search registered domain names by keyword and TLD for brand research, competitive analysis, domain squatting analysis, and domain name brainstorming.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup runs an unpinned third-party npm package locally.

Mitigation: Use a pinned and trusted mcp-remote version or a controlled installation path before deployment.

Risk: The MCP integration can access local filesystem, environment, or network capabilities depending on how it is run.

Mitigation: Run it with only the filesystem, environment variables, and network access required for domain search.

## Reference(s):

- [Pipeworx domains homepage](https://pipeworx.io/packs/domains)
- [Pipeworx domains MCP endpoint](https://gateway.pipeworx.io/domains/mcp)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include domain names, creation dates, and update timestamps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
