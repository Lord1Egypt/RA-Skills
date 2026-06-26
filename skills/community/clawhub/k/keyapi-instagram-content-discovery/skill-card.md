## Description: <br>
Explore and discover Instagram content at scale — search posts, Reels, hashtags, music, locations, and Explore sections to surface trends, audience signals, and high-engagement content opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content analysts use this skill to query KeyAPI's Instagram MCP service for post details, comments, hashtags, Reels, music, Explore sections, and location-based content discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens and fetched Instagram data may be stored locally in .env or .keyapi-cache. <br>
Mitigation: Use a least-privilege KeyAPI token, keep the skill directory out of source control, and regularly delete .env and .keyapi-cache contents that should not be retained. <br>
Risk: Exported API results can contain sensitive social-media data. <br>
Mitigation: Review exported results before sharing or committing them and handle them according to the intended privacy and retention policy. <br>
Risk: The bundled runner exposes broader MCP calling behavior than the Instagram-only purpose suggests. <br>
Mitigation: Review tool invocations before execution and restrict use to the documented Instagram discovery workflow. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/lycici/keyapi-instagram-content-discovery) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI Instagram MCP endpoint](https://mcp.keyapi.ai/instagram/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save API responses to a local .keyapi-cache directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
