## Description: <br>
Discover, profile, and analyze TikTok influencers with keyword search, profile lookup, follower trends, engagement rates, live-stream GMV, video performance, and competitive ranking workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, creator-commerce, and competitive-intelligence users can discover TikTok influencers, resolve creator identities, compare performance metrics, and produce structured campaign-fit analysis. The skill is most useful when an agent needs to orchestrate KeyAPI MCP calls and synthesize influencer research into a concise report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A KeyAPI bearer token may be stored in a local plaintext .env file. <br>
Mitigation: Set KEYAPI_TOKEN in the shell when possible, keep any .env file private, and avoid committing local credential files. <br>
Risk: API research results are cached on disk by default and may include sensitive creator or campaign research. <br>
Mitigation: Use --no-cache for sensitive runs or clear the .keyapi-cache directory after use. <br>
Risk: Changing KEYAPI_SERVER_URL can send authenticated requests to a non-default service. <br>
Mitigation: Keep KEYAPI_SERVER_URL at the default unless the replacement endpoint is trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lycici/keyapi-tiktok-influencer-discovery) <br>
- [KeyAPI Website](https://keyapi.ai/) <br>
- [KeyAPI MCP Service](https://mcp.keyapi.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research reports with command examples and JSON API result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses KEYAPI_TOKEN authentication, Node.js execution, optional local cache files, and KeyAPI MCP responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
