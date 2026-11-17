## Description:

Analyze YouTube videos in depth to retrieve metadata, comments, sub-comment threads, stream formats, related recommendations, Shorts results, search results, and trending content across categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to gather YouTube video intelligence, inspect audience comments and replies, enumerate stream formats, discover related or trending content, and synthesize findings from KeyAPI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a real KeyAPI token and the security assessment flags token handling for review.

Mitigation: Set KEYAPI_TOKEN only for the command invocation or trusted shell session, and avoid flows that persist the token to a local .env file.

Risk: Changing KEYAPI_SERVER_URL can direct requests and credentials to an untrusted endpoint.

Mitigation: Do not set KEYAPI_SERVER_URL unless the endpoint is explicitly trusted.

Risk: Cached or output JSON can contain private API results.

Mitigation: Treat generated caches and saved outputs as sensitive data and remove or protect them after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lycici/skills/keyapi-youtube-video-analysis)
- [KeyAPI](https://keyapi.ai/)
- [KeyAPI YouTube MCP server](https://mcp.keyapi.ai/youtube/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with inline shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local cached result files containing API responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
