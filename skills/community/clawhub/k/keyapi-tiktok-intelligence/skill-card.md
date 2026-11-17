## Description:

Real-time TikTok trend intelligence — monitor trending hashtags, viral music, breakout videos, top-performing ads, and high-growth products to identify emerging opportunities and market movements before they become mainstream.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

External users, brands, creators, analysts, and developers use this skill to gather TikTok trend, commerce, and ad intelligence through KeyAPI for market research and campaign planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: KeyAPI credentials may be exposed if saved in plaintext or used in an untrusted environment.

Mitigation: Set KEYAPI_TOKEN only in a trusted shell or secret manager, and avoid the interactive plaintext .env save flow.

Risk: Changing KEYAPI_SERVER_URL can send authenticated requests to an untrusted destination.

Mitigation: Use the default KeyAPI MCP endpoint unless the replacement endpoint is fully trusted.

Risk: Cached TikTok market research may remain on disk after analysis.

Mitigation: Clear, protect, or relocate .keyapi-cache when cached intelligence should not persist locally.

Risk: Available remote tools may be broader than the TikTok-focused description suggests.

Mitigation: Review the tool list and input schemas before invoking tools, and call only the endpoints needed for the specific analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lycici/skills/keyapi-tiktok-intelligence)
- [KeyAPI](https://keyapi.ai/)
- [KeyAPI MCP Server](https://mcp.keyapi.ai)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown briefings with optional JSON API results and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include time-sensitive TikTok intelligence cached locally by date.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
