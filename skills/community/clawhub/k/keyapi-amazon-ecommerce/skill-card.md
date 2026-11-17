## Description:

Explore and analyze Amazon e-commerce data at scale for product search, category browsing, product details, best sellers, deals, seller intelligence, influencer storefronts, reviews, and ASIN/GTIN conversion across 24 Amazon marketplaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and marketplace researchers use this skill to query KeyAPI's Amazon MCP service and prepare e-commerce intelligence reports on products, sellers, reviews, deals, offers, and influencer storefronts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a KeyAPI token and can write it to a local .env file during interactive setup.

Mitigation: Set KEYAPI_TOKEN through the environment or a secure secret store and do not commit any .env file.

Risk: KEYAPI_SERVER_URL can redirect requests and tokens to a different MCP server.

Mitigation: Leave KEYAPI_SERVER_URL unset unless you intentionally trust the specific replacement server.

Risk: Local API response caches may retain retrieved marketplace data under .keyapi-cache.

Mitigation: Review, exclude, or delete cache files before sharing the workspace or committing outputs.

Risk: The security summary notes that the runner is broader than the Amazon-only description.

Mitigation: Review the requested platform and tool before execution and install only if you trust KeyAPI and the publisher.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lycici/skills/keyapi-amazon-ecommerce)
- [KeyAPI](https://keyapi.ai/)
- [KeyAPI Amazon MCP server](https://mcp.keyapi.ai/amazon/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save API responses to local JSON output files and date-partitioned .keyapi-cache entries.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
