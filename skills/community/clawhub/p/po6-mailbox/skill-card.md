## Description: <br>
Manage PO6 email aliases, mailbox, and landing pages via the PO6 MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[winstein](https://clawhub.ai/user/winstein) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect OpenClaw to PO6 for mailbox, alias, domain, and landing page operations through natural language. It supports reading, searching, sending, replying, forwarding, drafting, alias administration, domain configuration, page publishing, analytics, and lead review when the user's PO6 API key has the required scopes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive mailbox content and account configuration when the PO6 API key includes broad scopes. <br>
Mitigation: Create a PO6 API key with only the scopes required for the intended workflow, starting with read-only scopes when possible. <br>
Risk: Sending, deleting, publishing, archiving, or domain-assignment actions can affect external recipients or public content. <br>
Mitigation: Use drafts and review flows where available, and rely on the documented two-step confirmation for destructive or publishing actions. <br>
Risk: A leaked or stale PO6 API key could permit mailbox, alias, domain, or landing page operations within its granted scopes. <br>
Mitigation: Keep PO6_API_KEY local, verify the MCP endpoint is https://mcp.po6.com, and rotate or revoke the key when access is no longer needed. <br>


## Reference(s): <br>
- [PO6 MCP Documentation](https://po6.com/docs/mcp) <br>
- [PO6 Website](https://po6.com) <br>
- [PO6 Dashboard](https://po6.com/dashboard) <br>
- [ClawHub Skill Page](https://clawhub.ai/winstein/po6-mailbox) <br>
- [Publisher Profile](https://clawhub.ai/user/winstein) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and MCP-backed tool results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PO6_API_KEY and communicates with https://mcp.po6.com.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
