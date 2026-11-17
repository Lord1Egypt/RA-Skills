## Description:

Provides TikTok Shop ERP OAuth authorization, authorized ERP store listing, and optional token lookup or manual token refresh for LinkFox-powered agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and developers use this skill to authorize TikTok Shop ERP stores, list authorized ERP stores, and prepare an openId for downstream ERP business skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential and token-related data can be exposed if API key environment variables or generated response files are mishandled.

Mitigation: Protect LINKFOX_AGENT_API_KEY/LINKFOXAGENT_API_KEY and treat generated LinkFox output directories as sensitive.

Risk: Overriding LINKFOX_TOOL_GATEWAY or TIKTOK_SHOP_API_BASE_URL can send credentialed requests to an untrusted endpoint.

Mitigation: Set gateway override variables only to destinations you control.

Risk: Manual token lookup or refresh can expose token-related responses and should not be used as a routine business prerequisite.

Mitigation: Use token lookup and manual refresh only for diagnostics or explicit user requests; rely on openId-based downstream business calls for normal use.

## Reference(s):

- [TikTok Shop ERP Authorization API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-tiktok-shop-auth)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Displayed token values are masked, but generated response files can contain authorization URLs, seller identifiers, token-related responses, and error details.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
