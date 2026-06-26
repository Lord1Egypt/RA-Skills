## Description: <br>
Discover, profile, and deeply analyze Instagram users by exploring follower and following networks, posts, Reels, Stories, Highlights, tagged content, reposts, and similarity-based recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect Instagram profile, content, social graph, and similarity data through the KeyAPI MCP service, then synthesize structured user intelligence reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a broader MCP runner and can make authenticated requests to KeyAPI services. <br>
Mitigation: Install only when you trust KeyAPI, set KEYAPI_TOKEN through the environment, and use --platform instagram explicitly. <br>
Risk: Sensitive lookup results and credentials may be stored locally through .keyapi-cache or .env. <br>
Mitigation: Use --no-cache for sensitive lookups, keep KEYAPI_TOKEN out of source control, and delete .keyapi-cache and .env when no longer needed. <br>
Risk: KEYAPI_SERVER_URL can redirect requests to an alternate endpoint. <br>
Mitigation: Avoid KEYAPI_SERVER_URL overrides unless the endpoint is known and trusted. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/lycici/keyapi-instagram-user-analysis) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI Instagram MCP server](https://mcp.keyapi.ai/instagram/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KEYAPI_TOKEN and Node.js; API responses may be cached locally under .keyapi-cache unless caching is disabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
