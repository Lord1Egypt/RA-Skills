## Description: <br>
Comprehensive TikTok Shop market intelligence - analyze products, shops, and categories with GMV, sales trends, reviews, creator attribution, and competitive ranking data across the full e-commerce ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, market researchers, and e-commerce analysts use this skill to query KeyAPI's TikTok Shop MCP tools, inspect product, shop, category, creator, video, and livestream commerce data, and synthesize market intelligence reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist a KeyAPI bearer token and cached business data locally. <br>
Mitigation: Set KEYAPI_TOKEN only for the active session when possible, do not commit .env files, and periodically delete .keyapi-cache and output files containing market data. <br>
Risk: Authenticated requests can be redirected by KEYAPI_SERVER_URL. <br>
Mitigation: Leave KEYAPI_SERVER_URL unset unless the endpoint is fully trusted. <br>
Risk: Cached market research results may contain sensitive commercial analysis. <br>
Mitigation: Use --no-cache for sensitive research or store outputs only in approved locations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lycici/keyapi-tiktok-ecommerce) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI MCP Server](https://mcp.keyapi.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSON cache files and optional output files containing TikTok Shop market data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
