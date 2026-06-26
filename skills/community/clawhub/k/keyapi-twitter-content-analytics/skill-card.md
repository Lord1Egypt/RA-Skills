## Description: <br>
Explore and analyze Twitter/X content at scale by retrieving user profiles, tweets, comments, replies, media, search results, trending topics, and follower or following networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research teams use this skill to collect and summarize Twitter/X profiles, tweets, replies, comments, trends, search results, and social graph data through the KeyAPI MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a KeyAPI token for Twitter/X research and can load or save that token locally. <br>
Mitigation: Set KEYAPI_TOKEN in the shell when possible, keep any .env file private, and avoid committing the skill directory. <br>
Risk: Cached Twitter/X lookup results can remain on disk after analysis. <br>
Mitigation: Use --no-cache for sensitive lookups and periodically delete .keyapi-cache when cached social data should not remain locally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lycici/keyapi-twitter-content-analytics) <br>
- [Publisher profile](https://clawhub.ai/user/lycici) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI Twitter MCP endpoint](https://mcp.keyapi.ai/twitter/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write API responses to local cache files and optional output files when the runner is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
