## Description: <br>
Discover and analyze TikTok Shop creators — identify top-performing commerce sellers, evaluate GMV and sales metrics, understand audience demographics, and track creator growth trends within the TikTok e-commerce ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover TikTok Shop creators, resolve creator identifiers, and evaluate commerce performance, audience demographics, growth trends, and promotion-video effectiveness for partnership decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a broad KeyAPI MCP runner that can call more than the advertised creator-discovery tools. <br>
Mitigation: Review intended tool calls before use and verify KEYAPI_SERVER_URL is unset or points only to a trusted KeyAPI endpoint. <br>
Risk: API tokens and query results may be stored or loaded locally through environment variables, .env, and .keyapi-cache. <br>
Mitigation: Prefer setting KEYAPI_TOKEN in the shell, keep .env out of source control, and clear .keyapi-cache before sharing the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lycici/keyapi-tiktok-shop-creator-discovery) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI MCP server](https://mcp.keyapi.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and JSON API-call results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cache API responses and converted image URLs locally under .keyapi-cache.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
