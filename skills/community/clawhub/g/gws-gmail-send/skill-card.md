## Description: <br>
Gmail: Send an email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using Google Workspace use this skill to prepare Gmail send commands through the gws CLI, including recipients, subject, body, sender alias, CC/BCC, attachments, HTML content, dry runs, and drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email can be sent from the active Gmail account or configured sender alias to unintended recipients. <br>
Mitigation: Confirm the active account, sender alias, recipients, subject, body, and attachments before sending. <br>
Risk: Attachments, HTML body content, or send-as aliases can expose sensitive information if used incorrectly. <br>
Mitigation: Use --dry-run or --draft when review is needed before sending the message. <br>
Risk: The skill depends on the gws CLI and shared Gmail authentication setup. <br>
Mitigation: Install only if the gws CLI is trusted and review the generated shared Gmail/auth instructions before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-gmail-send) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands that send mail should be confirmed with the user before execution.] <br>

## Skill Version(s): <br>
1.0.15 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
