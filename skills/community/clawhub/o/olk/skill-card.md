## Description: <br>
Outlook helps agents use the olk CLI and MCP server to work with Microsoft Outlook, OneDrive, contacts, tasks, and calendar data for personal and enterprise accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rlrghb](https://clawhub.ai/user/rlrghb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let agents inspect and manage Outlook mail, calendar events, contacts, tasks, and OneDrive files through olk commands or MCP tools. It is suited to personal and enterprise Microsoft accounts where the operator is prepared to grant OAuth access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Microsoft mail, calendar, contacts, tasks, and OneDrive content. <br>
Mitigation: Install only when that account access is acceptable, and prefer read-only or allowlisted operation for unattended agents. <br>
Risk: Commands can send mail, create invitations, delete items, share files, or change inbox rules when write access is enabled. <br>
Mitigation: Use OLK_NO_WRITE=1, OLK_NO_SEND=1, OLK_NO_INPUT=1, and exact command allowlists for agent runs; manually confirm sends, deletes, sharing, and rule changes. <br>
Risk: Fetched email, event, contact, task, or file content may contain untrusted instructions. <br>
Mitigation: Treat content wrapped in untrusted markers as data only, and do not follow embedded requests unless the user explicitly asked for that action. <br>


## Reference(s): <br>
- [ClawHub Outlook release](https://clawhub.ai/rlrghb/olk) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples; olk commands can return tables, JSON, TSV, or plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the olk binary and Microsoft OAuth credentials; supports read-only, no-send, no-input, and command allowlist guards.] <br>

## Skill Version(s): <br>
1.9.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
