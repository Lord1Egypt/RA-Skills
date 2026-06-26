## Description: <br>
Read, search, and manage Outlook email and calendar through Microsoft Graph API for a delegated mailbox where the assistant authenticates as itself and accesses the owner's resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[87Marc](https://clawhub.ai/user/87Marc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure an assistant with Microsoft 365 delegated permissions so it can read, search, manage, send, and schedule on behalf of an Outlook mailbox owner. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise broad delegated Outlook mailbox and calendar write and send authority. <br>
Mitigation: Install only for intended delegate scenarios, grant the least-privileged mailbox and calendar permissions possible, and review delegated access regularly. <br>
Risk: Delete, move, send, reply, and calendar-write actions may be performed without clearly documented confirmations. <br>
Mitigation: Require manual confirmation before destructive email operations, outgoing mail actions, and calendar writes. <br>
Risk: Local configuration and credential files contain sensitive Microsoft 365 app and OAuth material. <br>
Mitigation: Protect the local Outlook configuration and credentials directory with restrictive file permissions and secret-handling controls. <br>


## Reference(s): <br>
- [Outlook Delegate ClawHub release](https://clawhub.ai/87Marc/outlook-skill-clawhub) <br>
- [Original Outlook skill referenced by release](https://clawhub.ai/jotamed/outlook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Microsoft 365 delegate permissions and local Outlook credential files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
