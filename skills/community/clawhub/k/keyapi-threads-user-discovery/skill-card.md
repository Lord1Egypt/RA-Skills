## Description: <br>
Discover and analyze Threads users and content by retrieving profiles, posts, reposts, replies, post details, comments, and keyword search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to gather and summarize Threads profile, post, comment, and keyword-search data through KeyAPI MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A KeyAPI token is required and may be stored locally if entered through the helper prompt. <br>
Mitigation: Set KEYAPI_TOKEN through a shell or secret manager and avoid committing or sharing local .env files. <br>
Risk: Threads research results may be stored in .keyapi-cache or explicit output files. <br>
Mitigation: Use --no-cache for sensitive research and delete cache or output files when they are no longer needed. <br>
Risk: KEYAPI_SERVER_URL overrides or non-Threads platform arguments can route calls outside the documented Threads workflow. <br>
Mitigation: Avoid KEYAPI_SERVER_URL overrides and use --platform threads with the documented tools unless reviewing another endpoint deliberately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lycici/keyapi-threads-user-discovery) <br>
- [Publisher profile](https://clawhub.ai/user/lycici) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI Threads MCP endpoint](https://mcp.keyapi.ai/threads/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call KeyAPI MCP tools, print JSON responses, and write cached response files locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
