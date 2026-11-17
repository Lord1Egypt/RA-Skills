## Description:

Discover and analyze TikTok Shop creators to identify commerce sellers, evaluate GMV and sales metrics, understand audience demographics, and track creator growth trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and commerce teams use this skill to research TikTok Shop creators for seller discovery, creator audits, audience fit, sales performance, growth trends, and partnership recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner can use a broad KeyAPI MCP interface rather than only one narrow creator-analysis operation.

Mitigation: Review the skill before installing and inspect requested tool calls before providing credentials or running commands.

Risk: The KeyAPI token may be persisted in a plaintext .env file if entered interactively.

Mitigation: Use a dedicated, revocable KeyAPI token and prefer setting KEYAPI_TOKEN through the shell or a secret manager.

Risk: Creator analytics, audience data, and API responses may remain on disk in the local cache.

Mitigation: Clear .keyapi-cache after use when cached creator or audience data should not be retained.

Risk: Changing KEYAPI_SERVER_URL can redirect authenticated requests to a different endpoint.

Mitigation: Do not set KEYAPI_SERVER_URL unless the destination is fully trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lycici/skills/keyapi-tiktok-shop-creator-discovery)
- [KeyAPI](https://keyapi.ai/)
- [KeyAPI MCP server](https://mcp.keyapi.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured creator analysis reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cache API responses and creator analytics locally when the runner is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
