## Description: <br>
Personal productivity app with Ideas/Tasks, Journal, Habits, Package tracking, Lists, and more via MCP <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dgershman](https://clawhub.ai/user/dgershman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to connect an AI assistant to a Pndr account through MCP so the assistant can help manage tasks, habits, journal entries, packages, lists, and related productivity data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the skill allows an AI assistant to read, change, and delete data in the user's Pndr account. <br>
Mitigation: Use a dedicated or revocable OAuth token and require confirmation before deleting, archiving, bulk editing, or downloading attachments. <br>
Risk: OAuth client secrets and bearer tokens could be exposed through normal assistant conversation. <br>
Mitigation: Keep client secrets and bearer tokens out of ordinary chat and store them only in the MCP client configuration. <br>


## Reference(s): <br>
- [Pndr ClawHub Listing](https://clawhub.ai/dgershman/pndr) <br>
- [Pndr Homepage](https://pndr.io) <br>
- [Pndr Documentation](https://pndr.io/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an MCP-capable assistant and mcporter for manual setup.] <br>

## Skill Version(s): <br>
1.0.20260202 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
