## Description: <br>
Automate Microsoft 365 mailbox tasks via Microsoft Graph for Business and Consumer accounts, including reading, searching, creating drafts, and sending messages with device-code authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tradmangh](https://clawhub.ai/user/tradmangh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, developers, and mailbox operators use this skill to let an agent inspect unread mail, search messages, retrieve message details, create drafts, and send prepared drafts across Microsoft 365 Business or Consumer mailboxes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Granting Microsoft Graph mailbox permissions can expose or modify mailbox contents. <br>
Mitigation: Use minimal consent, avoid offline_access unless needed, and enable only the read, draft, or send capabilities required for the task. <br>
Risk: Draft creation can modify a mailbox without enforcing the confirmation safeguard implied by setup. <br>
Mitigation: Review draft permissions before enabling them and inspect created drafts before sending or allowing broader mailbox actions. <br>
Risk: Local token caches can grant continuing mailbox access if exposed. <br>
Mitigation: Protect the local token cache under ~/.openclaw/secrets/m365-mailbox/ and delete it when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tradmangh/m365-mailbox) <br>
- [Microsoft Graph Mail Endpoint](https://graph.microsoft.com/v1.0/me) <br>
- [Microsoft Device Login](https://microsoft.com/devicelogin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local Microsoft authentication profiles and Microsoft Graph mailbox permissions selected during setup.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
