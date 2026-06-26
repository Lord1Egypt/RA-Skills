## Description: <br>
Use the Mailbird MCP server running locally inside the Mailbird email client for email-related tasks such as inbox triage, sending, search, drafts, attachments, and contacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mailbirdagent](https://clawhub.ai/user/mailbirdagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent work with a local Mailbird mailbox through Mailbird's MCP server for reading, searching, drafting, sending, and managing email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Providing the Mailbird MCP token gives an agent broad access to the user's mailbox, including messages, contacts, attachments, drafts, and write actions when enabled. <br>
Mitigation: Install only when mailbox access is intended, keep the token private, do not share it with remote agents, and review drafts or destructive actions before allowing writes. <br>
Risk: Exposing the local MCP endpoint outside loopback could make mailbox access available beyond the local machine. <br>
Mitigation: Keep MAILBIRD_MCP_URL pointed at 127.0.0.1 or localhost and do not proxy, tunnel, or port-forward the endpoint. <br>


## Reference(s): <br>
- [Mailbird ClawHub listing](https://clawhub.ai/mailbirdagent/mailbird-mcp) <br>
- [Mailbird website](https://www.getmailbird.com) <br>
- [Mailbird local MCP endpoint default](http://127.0.0.1:18790/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, text] <br>
**Output Format:** [Markdown guidance with environment-variable configuration and MCP tool-use instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAILBIRD_MCP_TOKEN for authenticated mailbox access and optionally MAILBIRD_MCP_URL for a local loopback endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
