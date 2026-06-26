## Description: <br>
Outlook (microsoft.com) supports Outlook requests for reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to read Outlook account, mailbox, folder, and message data, and to create, update, send, or reply to Outlook emails through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can change Outlook mailbox state by creating, updating, sending, or replying to email. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running actions tagged as write. <br>
Risk: Connector access depends on user authentication, Outlook connection status, scopes, and account billing. <br>
Mitigation: Use the documented first-time setup and troubleshooting steps only when an action fails for the matching auth, connection, scope, or billing reason. <br>
Risk: The scanner reported clean evidence, but installation and account access are still not risk-free. <br>
Mitigation: Review the displayed skill instructions at install time and only approve account access, network calls, or write actions that match expected behavior. <br>


## Reference(s): <br>
- [ClawHub Outlook skill page](https://clawhub.ai/oomol/oo-outlook) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Microsoft Outlook](https://www.microsoft.com/microsoft-365/outlook/email-and-calendar-software-microsoft-outlook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before execution and returns connector responses as JSON when actions run.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
