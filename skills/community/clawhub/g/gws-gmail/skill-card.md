## Description: <br>
Gmail: Send, read, and manage email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to inspect Gmail commands, send and read messages, manage drafts, labels, settings, threads, and mailbox watches through the `gws` CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authenticated Gmail mailbox control. <br>
Mitigation: Install only if the `gws` CLI is trusted, verify the Gmail account and OAuth scopes in use, and require explicit confirmation before sending, forwarding, replying, changing settings, deleting mail, or watching a mailbox. <br>
Risk: Mailbox watch or streaming setup can continue after the immediate task is complete. <br>
Mitigation: Disable watch or streaming configuration when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-gmail) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the `gws` CLI and an authenticated Gmail account with appropriate OAuth scopes.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
