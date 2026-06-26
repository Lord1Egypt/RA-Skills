## Description: <br>
Explore and analyze Reddit content at scale by retrieving post details, comments, nested sub-comment threads, user activity, and curated Reddit feeds through KeyAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and researchers use this skill to collect Reddit post, comment, feed, subreddit, and user activity data, then synthesize structured content intelligence reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The KeyAPI token can call broader KeyAPI MCP platforms beyond the Reddit workflow. <br>
Mitigation: Use a limited KEYAPI_TOKEN where possible and keep calls explicitly scoped to --platform reddit. <br>
Risk: Cached Reddit queries and results can reveal sensitive research interests or user profiling activity. <br>
Mitigation: Avoid storing tokens or cache data on shared machines, and delete or disable .keyapi-cache when results are sensitive. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lycici/keyapi-reddit-content-analytics) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI Reddit MCP endpoint](https://mcp.keyapi.ai/reddit/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Files] <br>
**Output Format:** [Markdown reports with inline shell commands and JSON API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local cache files for fetched API responses when caching is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
