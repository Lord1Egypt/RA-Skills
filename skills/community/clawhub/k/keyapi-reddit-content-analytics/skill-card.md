## Description:

Explore and analyze Reddit content at scale, including post details, comments, sub-comment threads, user activity, and curated Reddit feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve Reddit posts, comments, nested replies, user activity, and feed data through the KeyAPI MCP service, then synthesize content intelligence reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled runner is broader than a tightly scoped Reddit-only helper and can use a custom KEYAPI_SERVER_URL.

Mitigation: Use the default trusted KeyAPI endpoint unless a custom endpoint has been reviewed, and confirm the intended platform and tool before running commands.

Risk: KEYAPI_TOKEN is required and the runner can load it from the environment or a local .env file.

Mitigation: Provide the token through an environment variable or secure secret manager, avoid interactive entry on shared systems, and rotate the token if it is exposed.

Risk: Cached API responses may contain Reddit user, comment, or post data.

Mitigation: Review or delete .keyapi-cache before sharing the workspace and avoid caching sensitive investigations unless retention is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lycici/skills/keyapi-reddit-content-analytics)
- [KeyAPI](https://keyapi.ai/)
- [KeyAPI Reddit MCP Server](https://mcp.keyapi.ai/reddit/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON API responses, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KEYAPI_TOKEN and Node.js 18 or higher; API responses may be cached locally under .keyapi-cache.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
