## Description:

Discover Instagram posts, Reels, hashtags, music, locations, and Explore sections to identify trends, engagement patterns, and audience signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, marketers, and developers use this skill to query KeyAPI Instagram MCP tools for post, comment, hashtag, music, Reels, Explore, and location research, then synthesize content intelligence from returned data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner uses a token-bearing KeyAPI connection and the security review says its authority is broader than the skill description suggests.

Mitigation: Review requested tool calls before execution, run under a normal user account, and provide KEYAPI_TOKEN through the environment instead of storing it in the skill directory.

Risk: KEYAPI_SERVER_URL can redirect the runner to an alternate MCP endpoint.

Mitigation: Leave KEYAPI_SERVER_URL unset unless the endpoint is fully trusted and reviewed.

Risk: Cached Instagram API responses may contain sensitive collected social data.

Mitigation: Treat .keyapi-cache as sensitive, restrict access to it, and delete cached files when they are no longer needed.

Risk: Dependencies are declared without a reviewed lockfile in the artifact evidence.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lycici/skills/keyapi-instagram-content-discovery)
- [KeyAPI](https://keyapi.ai/)
- [KeyAPI Instagram MCP Endpoint](https://mcp.keyapi.ai/instagram/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local .keyapi-cache JSON files when API calls are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
