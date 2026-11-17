## Description:

World country data for searching by name, code, region, language, or currency via REST Countries API v3.1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query country data for country selectors, location enrichment, language and currency questions, and geographic research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs an unpinned mutable third-party package with local user privileges.

Mitigation: Prefer a pinned, reviewed mcp-remote version or a locked local installation, and run the MCP bridge with only the permissions it needs.

## Reference(s):

- [Pipeworx Countries homepage](https://pipeworx.io/packs/countries)
- [Pipeworx Countries MCP endpoint](https://gateway.pipeworx.io/countries/mcp)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples; MCP tool calls return country data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Country lookups can include names, capitals, regions, populations, languages, currencies, flags, and geographic details.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
