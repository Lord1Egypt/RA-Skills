## Description: <br>
Explore and analyze public Facebook data, including profile details, posts, photos, Reels, group activity, group events, and identifier resolution for profiles and groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to query KeyAPI's Facebook MCP tools for public profile, page, and group data, then synthesize profile, content, engagement, and event findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Facebook URLs, IDs, and query parameters submitted through this skill are sent to KeyAPI. <br>
Mitigation: Use the skill only with public data and only when you trust KeyAPI with the submitted inputs. <br>
Risk: KEYAPI_TOKEN is required and may be loaded from the shell or a local .env file. <br>
Mitigation: Set the token through a shell or secrets manager, avoid committing .env files, and rotate the token if it is exposed. <br>
Risk: API responses are cached locally in .keyapi-cache by default. <br>
Mitigation: Review cached files for sensitive context and clear .keyapi-cache when the retained results are no longer needed. <br>
Risk: KEYAPI_SERVER_URL can redirect requests to a different MCP endpoint. <br>
Mitigation: Leave KEYAPI_SERVER_URL unset unless the alternate endpoint is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lycici/keyapi-facebook-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/lycici) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI Facebook MCP server](https://mcp.keyapi.ai/facebook/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KEYAPI_TOKEN and Node.js; caches API responses locally unless disabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
