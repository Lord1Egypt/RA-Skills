## Description:

Discover, profile, and deeply analyze TikTok influencers from keyword-based search to multi-dimensional performance intelligence covering follower trends, engagement rates, live-stream GMV, video performance, and competitive rankings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research TikTok creators for influencer discovery, campaign shortlisting, affiliate evaluation, and competitive performance analysis. It helps agents query KeyAPI, cache responses, and synthesize creator profile, trend, video, livestream, product, audience, and ranking insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a KeyAPI token and may store API responses locally.

Mitigation: Set KEYAPI_TOKEN through the environment, keep any .env file out of source control, and review or clear .keyapi-cache when creator or audience research is sensitive.

Risk: Changing KEYAPI_SERVER_URL sends authentication and research queries to a different destination.

Mitigation: Use the default KeyAPI MCP server unless the alternate server is fully trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lycici/skills/keyapi-tiktok-influencer-discovery)
- [KeyAPI](https://keyapi.ai/)
- [KeyAPI MCP server](https://mcp.keyapi.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses KEYAPI_TOKEN, Node.js, KeyAPI MCP calls, local response caching, pagination, and cover-image URL conversion.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
