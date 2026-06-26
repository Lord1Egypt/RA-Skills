## Description: <br>
Real-time TikTok trend intelligence — monitor trending hashtags, viral music, breakout videos, top-performing ads, and high-growth products to identify emerging opportunities and market movements before they become mainstream. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Brands, creators, analysts, and agents use this skill to gather TikTok trend, product, keyword, music, video, and ad intelligence through KeyAPI and turn the results into timely market briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill wraps a broad KeyAPI MCP runner, which can reach more tools than the TikTok-specific title implies. <br>
Mitigation: Keep use scoped to the documented TikTok intelligence tools and review selected tool names and parameters before execution. <br>
Risk: The runner can save KEYAPI_TOKEN to a plaintext local .env file and can write cached API responses under .keyapi-cache. <br>
Mitigation: Prefer environment variables or a secret manager for KEYAPI_TOKEN, avoid entering secrets interactively, and delete local .env and .keyapi-cache files when they are no longer needed. <br>
Risk: KEYAPI_SERVER_URL can redirect the MCP client to a different server. <br>
Mitigation: Use the default KeyAPI MCP server unless you control and trust the override endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lycici/keyapi-tiktok-intelligence) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI MCP server](https://mcp.keyapi.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefings, JSON API responses, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cached, timestamped TikTok intelligence snapshots and converted cover-image URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
