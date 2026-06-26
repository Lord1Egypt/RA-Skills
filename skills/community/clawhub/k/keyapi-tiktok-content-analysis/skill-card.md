## Description: <br>
Analyze TikTok content at scale, including videos, hashtags, music tracks, live streams, engagement trends, comment sentiment, caption transcription, and commerce attribution data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and marketing teams use this skill to retrieve and synthesize TikTok performance, audience, hashtag, music, live-stream, and commerce signals through KeyAPI-backed tool calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a KeyAPI token and may access broader remote MCP server capabilities than TikTok analysis alone. <br>
Mitigation: Use a rotatable, least-privilege token and inspect available tools before issuing calls. <br>
Risk: Credentials may be loaded from a plaintext .env file and API responses may be retained in a local cache. <br>
Mitigation: Avoid high-value tokens, restrict local file access, and clear .keyapi-cache when cached TikTok data should not persist. <br>


## Reference(s): <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI MCP Server](https://mcp.keyapi.ai) <br>
- [ClawHub skill page](https://clawhub.ai/lycici/keyapi-tiktok-content-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and KEYAPI_TOKEN; tool calls may cache API responses locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
