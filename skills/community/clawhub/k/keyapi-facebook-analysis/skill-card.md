## Description:

Explore and analyze public Facebook data, including profile details, posts, photos, Reels, group activity, group events, and identifier resolution for profiles and groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve and summarize public Facebook profile, page, and group data through the KeyAPI MCP service. It supports profile and group lookup, content feed analysis, event discovery, and identifier resolution for downstream API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner requires a KeyAPI token and may persist it locally if entered interactively.

Mitigation: Use a scoped KeyAPI token and set it through the environment instead of interactive entry.

Risk: Custom KEYAPI_SERVER_URL values can redirect API calls and credentials to a non-default endpoint.

Mitigation: Use the default KeyAPI MCP endpoint unless the replacement server is fully trusted.

Risk: Cached response files may contain public-profile research results.

Mitigation: Treat local cache and output files as data artifacts and remove them when they are no longer needed.

## Reference(s):

- [KeyAPI](https://keyapi.ai/)
- [KeyAPI Facebook MCP server](https://mcp.keyapi.ai/facebook/mcp)
- [ClawHub skill page](https://clawhub.ai/lycici/skills/keyapi-facebook-analysis)
- [Publisher profile](https://clawhub.ai/user/lycici)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, analysis, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local cache and output JSON files when the runner is used with caching or output options.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
