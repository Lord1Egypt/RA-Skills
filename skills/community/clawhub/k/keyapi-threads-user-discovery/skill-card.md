## Description:

Discover and analyze Threads users and content by retrieving user profiles, posts, reposts, replies, post details, comments, and keyword search results across top content, recent content, and user profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to collect and synthesize Threads profile, post, comment, and keyword-search data through KeyAPI for social content research and discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper uses KEYAPI_TOKEN to call KeyAPI services, and the security summary warns that token use may be broader or less protected than the skill description makes clear.

Mitigation: Review before installing, use a scoped KeyAPI token, and provide KEYAPI_TOKEN through a shell environment or secret manager rather than the interactive prompt.

Risk: KEYAPI_SERVER_URL can redirect API calls and token-bearing requests to a different endpoint.

Mitigation: Leave KEYAPI_SERVER_URL unset unless the destination is fully trusted.

Risk: The helper can persist API responses and tokens in local .keyapi-cache or .env files.

Mitigation: Clear .keyapi-cache and .env files when they are no longer needed, especially on shared systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lycici/skills/keyapi-threads-user-discovery)
- [KeyAPI](https://keyapi.ai/)
- [KeyAPI Threads MCP server](https://mcp.keyapi.ai/threads/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API response handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include locally cached API responses and synthesized profile, post, comment, engagement, and search findings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
