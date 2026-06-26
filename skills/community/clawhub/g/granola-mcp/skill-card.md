## Description: <br>
Access Granola AI meeting notes through MCP, including meeting search, date-range listing, full meeting details, verbatim transcripts, and OAuth token refresh guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bholagabbar](https://clawhub.ai/user/bholagabbar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and agents with authorized Granola access use this skill to answer questions about meeting notes, action items, decisions, and transcripts from their workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The OAuth and mcporter configuration files contain access tokens and other secrets. <br>
Mitigation: Keep config/granola_oauth.json and config/mcporter.json private, and do not commit or share them. <br>
Risk: The token refresh script posts credentials to the configured token endpoint. <br>
Mitigation: Verify the token endpoint is Granola's official HTTPS endpoint before refreshing credentials. <br>
Risk: Periodic token refresh can maintain background access to meeting data. <br>
Mitigation: Enable scheduled refresh only when the workspace owner is comfortable with ongoing access renewal. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bholagabbar/granola-mcp) <br>
- [Granola OAuth authorization endpoint](https://mcp-auth.granola.ai/oauth2/authorize) <br>
- [Granola OAuth token endpoint](https://mcp-auth.granola.ai/oauth2/token) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with citation links, plus MCP call arguments and shell commands for token refresh.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Granola citation links and verbatim transcript excerpts when requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
