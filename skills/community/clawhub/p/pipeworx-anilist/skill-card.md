## Description:

Search, retrieve, and get trending anime details including title, episodes, status, score, genres, and synopsis via the AniList GraphQL API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure an AniList MCP server for searching anime, retrieving details by ID, and finding currently trending anime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Anime search terms and lookup requests are sent to gateway.pipeworx.io rather than directly to AniList.

Mitigation: Avoid sending private or unrelated information through the tool.

Risk: Returned lookup text is external data and could be unreliable or inappropriate to treat as instructions.

Mitigation: Use returned anime details as reference data and review them before acting on them.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/b-gutman/skills/pipeworx-anilist)
- [Pipeworx AniList MCP gateway](https://gateway.pipeworx.io/anilist/mcp)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Markdown with a JSON MCP server configuration block and text lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Anime lookup requests are routed through gateway.pipeworx.io.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
