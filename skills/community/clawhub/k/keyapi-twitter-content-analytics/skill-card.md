## Description:

Explore and analyze Twitter/X content at scale by retrieving user profiles, tweets, comments, replies, media, search results, trends, and follower/following networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and social-media researchers use this skill to gather Twitter/X posts, profiles, comments, trends, and social graph data through KeyAPI MCP, then summarize engagement, conversation, and discovery findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a KeyAPI token and may load it from a local .env file.

Mitigation: Set KEYAPI_TOKEN in the shell where possible, and protect or delete any .env file created in the skill directory.

Risk: Twitter/X query results can be stored in a local cache.

Mitigation: Treat cached results as potentially sensitive social data and delete or protect the .keyapi-cache directory when analysis is complete.

Risk: KEYAPI_SERVER_URL can point the runner at a non-default endpoint.

Mitigation: Use the default KeyAPI MCP endpoint unless you trust the alternate server.

Risk: The security summary says the bundled runner is broader than the Twitter-only description.

Mitigation: Review the bundled runner and limit use to intended KeyAPI Twitter/X workflows before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lycici/skills/keyapi-twitter-content-analytics)
- [KeyAPI](https://keyapi.ai/)
- [KeyAPI Twitter MCP endpoint](https://mcp.keyapi.ai/twitter/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local cache for retrieved KeyAPI results; requires KEYAPI_TOKEN and Node.js.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
