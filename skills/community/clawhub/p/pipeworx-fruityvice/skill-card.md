## Description:

Nutritional data for fruits — calories, sugar, fat, protein, and carbs per 100g from Fruityvice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query fruit nutrition data by fruit name, browse available fruits, or filter fruits by nutrient ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented setup runs an unpinned npm package at install or runtime, giving a mutable dependency local execution authority.

Mitigation: Use a pinned, reviewed mcp-remote version or run the MCP setup in an isolated environment, especially on machines with sensitive files, tokens, or project credentials.

## Reference(s):

- [Pipeworx Fruityvice homepage](https://pipeworx.io/packs/fruityvice)
- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-fruityvice)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown with inline shell, JSON configuration, and nutrition response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns fruit nutrition values per 100g when the remote Fruityvice MCP service is available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
