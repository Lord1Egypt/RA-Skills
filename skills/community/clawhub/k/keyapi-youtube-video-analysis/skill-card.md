## Description: <br>
Analyze YouTube videos at depth by retrieving metadata, comments, reply threads, stream formats, related recommendations, Shorts, search results, and trending content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to inspect YouTube videos, comments, related content, Shorts search results, and trending categories through KeyAPI. It supports video audits, audience and comment analysis, content discovery, and trend monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video, comment, search, and trend queries are sent to KeyAPI. <br>
Mitigation: Use the skill only when KeyAPI is an acceptable processor for the submitted queries, and avoid sending sensitive or private research targets unless approved. <br>
Risk: KEYAPI_TOKEN is required for bearer authentication and may be stored locally if placed in a .env file. <br>
Mitigation: Prefer setting KEYAPI_TOKEN in the environment, protect any local .env file, and rotate the token if it is exposed. <br>
Risk: API responses can be written to the local .keyapi-cache directory, creating a local record of requested videos, comments, searches, and trends. <br>
Mitigation: Use a disposable cache directory or remove .keyapi-cache after analysis when local retention is not appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lycici/keyapi-youtube-video-analysis) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI YouTube MCP Server](https://mcp.keyapi.ai/youtube/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and KEYAPI_TOKEN; local API responses may be cached under .keyapi-cache.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
