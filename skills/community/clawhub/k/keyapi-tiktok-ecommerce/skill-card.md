## Description:

Comprehensive TikTok Shop market intelligence - analyze products, shops, and categories with GMV, sales trends, reviews, creator attribution, and competitive ranking data across the full e-commerce ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business analysts use this skill to gather TikTok Shop market intelligence for product research, shop benchmarking, category analysis, review analysis, creator attribution, and live-commerce performance reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a KeyAPI token and can load credentials from environment variables or a local .env file.

Mitigation: Use a minimally scoped token, set KEYAPI_TOKEN only for the current command when possible, and do not commit or share .env files.

Risk: The skill can cache API responses locally, which may contain market research outputs or other sensitive working data.

Mitigation: Review cached files before sharing the workspace and do not commit or publish .keyapi-cache.

Risk: The security summary flags broader MCP access than the description suggests.

Mitigation: Review requested tool schemas and commands before execution, and only use KEYAPI_SERVER_URL with trusted endpoints.

Risk: The runner requires npm dependency installation before use.

Mitigation: Install dependencies in a contained environment and review dependency changes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lycici/skills/keyapi-tiktok-ecommerce)
- [KeyAPI](https://keyapi.ai/)
- [KeyAPI MCP server](https://mcp.keyapi.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cached API response files under .keyapi-cache when the runner is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
