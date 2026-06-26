## Description: <br>
Discover and analyze Reddit users and subreddits, including public user profiles, active communities, public trophies, subreddit rules, settings, post channels, typeahead suggestions, dynamic search, and trending search intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to collect and summarize Reddit user, subreddit, search, and trend intelligence through the KeyAPI Reddit MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reddit lookup queries and returned data are sent through the KeyAPI service using the configured KEYAPI_TOKEN. <br>
Mitigation: Install only when that data flow is acceptable and use the documented --platform reddit commands. <br>
Risk: Local .env and .keyapi-cache files can retain API tokens or Reddit lookup results on disk. <br>
Mitigation: Keep .env private, avoid committing local cache files, and use --no-cache or delete .keyapi-cache when results should not be retained. <br>
Risk: The reusable runner can call broader KeyAPI tools if invoked outside the Reddit workflow. <br>
Mitigation: Review commands before execution and restrict routine use to the documented Reddit platform and tool names. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lycici/keyapi-reddit-user-analysis) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI Reddit MCP endpoint](https://mcp.keyapi.ai/reddit/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local JSON cache files for KeyAPI responses when the runner is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
