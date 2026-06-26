## Description: <br>
Discover and analyze Pinterest users, pins, boards, followers, and following through KeyAPI MCP calls for profile lookup, content inventory, board review, and social graph analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to query Pinterest user, pin, board, follower, and following data and synthesize structured Pinterest intelligence reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included runner is broader than a locked-down Pinterest helper and can call KeyAPI MCP tools based on command options. <br>
Mitigation: Use commands with --platform pinterest and review requested tool names and parameters before execution. <br>
Risk: Credentials and API results can be stored locally through the .env loader and .keyapi-cache directory. <br>
Mitigation: Protect or delete the .env file and clear .keyapi-cache when cached Pinterest results should not remain on disk. <br>
Risk: An untrusted KEYAPI_SERVER_URL value can redirect MCP traffic away from the default KeyAPI service. <br>
Mitigation: Use the default https://mcp.keyapi.ai endpoint unless a trusted operator has approved a different server URL. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lycici/keyapi-pinterest-analysis) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI Pinterest MCP endpoint](https://mcp.keyapi.ai/pinterest/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cache API responses locally under .keyapi-cache and may write requested JSON output files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
