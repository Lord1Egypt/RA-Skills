## Description: <br>
Read, search, and manage Outlook emails and calendar via Microsoft Graph API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cristiandan](https://clawhub.ai/user/cristiandan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People and agents with Microsoft Outlook or Microsoft 365 accounts use this skill to inspect inbox content, search mail, send or manage messages, and view or update calendar events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants persistent read/write/send access to Outlook mail and read/write access to calendars. <br>
Mitigation: Install it only for accounts where that level of access is acceptable, and review Microsoft Graph permissions before authorizing the app. <br>
Risk: Client secrets and OAuth tokens are stored locally, and the token script can print access tokens. <br>
Mitigation: Treat ~/.outlook-mcp as sensitive, avoid printing or logging tokens, keep file permissions restricted, and rotate credentials if exposure is suspected. <br>
Risk: Mail and calendar commands can send, move, delete, or modify real account data. <br>
Mitigation: Verify exact recipients, message IDs, event IDs, folders, and calendar targets before running destructive or sending actions. <br>
Risk: Attachment handling or file writes may place sensitive content in unsafe locations. <br>
Mitigation: Avoid downloading attachments to sensitive paths and inspect destination paths before saving files. <br>


## Reference(s): <br>
- [Outlook Plus on ClawHub](https://clawhub.ai/cristiandan/outlook-plus) <br>
- [Outlook Manual Setup Guide](references/setup.md) <br>
- [Azure CLI installation](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Azure CLI and jq; stores account credentials under ~/.outlook-mcp.] <br>

## Skill Version(s): <br>
1.9.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
