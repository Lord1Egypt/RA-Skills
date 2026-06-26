## Description: <br>
Discover, profile, and analyze YouTube channels, including channel metadata, video libraries, channel ID and URL conversion, keyword search, and filtered YouTube search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content analysts use this skill to resolve YouTube channel identities, retrieve channel and video metadata, search channels, and synthesize channel research findings through KeyAPI MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled runner can access broader KeyAPI MCP tooling than the YouTube-focused skill purpose. <br>
Mitigation: Use explicit --platform youtube commands and avoid arbitrary tool names unless broader KeyAPI MCP access is intended. <br>
Risk: API tokens and YouTube research queries are shared with KeyAPI and may be sensitive. <br>
Mitigation: Install only when KeyAPI is trusted for the use case, and provide KEYAPI_TOKEN through an environment variable or secret manager. <br>
Risk: The skill can persist API results in a local .keyapi-cache directory. <br>
Mitigation: Use --no-cache for sensitive lookups or delete .keyapi-cache after analysis. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lycici/keyapi-youtube-channel-analysis) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI YouTube MCP endpoint](https://mcp.keyapi.ai/youtube/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses KEYAPI_TOKEN, Node.js, KeyAPI MCP calls, and optional local response caching.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
