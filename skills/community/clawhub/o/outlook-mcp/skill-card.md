## Description: <br>
Production-grade MCP server for personal Outlook accounts that gives agents typed Microsoft Graph tools for mail, calendar, contacts, to-do, drafts, attachments, folders, threading, batch operations, and delta sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mpalermiti](https://clawhub.ai/user/mpalermiti) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent builders and developers use this skill to connect MCP-compatible agents to personal Outlook.com, Hotmail, or Live accounts for email triage, calendar work, contact management, task tracking, drafts, attachments, and recurring inbox or calendar digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live access to personal Outlook data and account actions. <br>
Mitigation: Install only when that access is acceptable; begin with read_only=true and grant specific allow_categories only when write access is needed. <br>
Risk: Email sending, deletion, triage, calendar changes, task updates, and attachment operations can affect real account state. <br>
Mitigation: Avoid automatic sending or deletion workflows, review drafts and high-impact actions, and restrict write categories to the smallest practical set. <br>
Risk: OAuth tokens and downloaded attachments create local credential and file-handling exposure. <br>
Mitigation: Use encrypted OS credential storage for tokens, especially on Linux, and do not allow agents to choose arbitrary attachment save paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mpalermiti/outlook-mcp) <br>
- [MCP Registry entry](https://registry.modelcontextprotocol.io/v0/servers?search=mpalermiti) <br>
- [PyPI package](https://pypi.org/project/outlook-graph-mcp/) <br>
- [OpenClaw MCP docs](https://docs.openclaw.ai/cli/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Structured data, Text, Shell commands, Configuration] <br>
**Output Format:** [MCP tool calls and structured JSON-like responses, with setup guidance in Markdown and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a personal Microsoft account, a user-provided Azure app client ID, local OAuth authentication, and Python >=3.10.] <br>

## Skill Version(s): <br>
1.11.0 (source: server release evidence, pyproject.toml, CHANGELOG, and server.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
