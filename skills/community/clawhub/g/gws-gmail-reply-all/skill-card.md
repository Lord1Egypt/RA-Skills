## Description: <br>
Gmail: Reply-all to a message (handles threading automatically). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users with the GWS CLI and Gmail access use this skill to prepare reply-all messages in existing Gmail threads, including adding or removing recipients, attaching files, choosing HTML or plain text, and saving as a draft when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help send email through the external GWS CLI, so mistakes in account, sender alias, recipients, message body, or attachments may send unintended content. <br>
Mitigation: Use --dry-run or --draft for sensitive threads, and verify the active Gmail account, sender alias, recipients, body, and attachments before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-gmail-reply-all) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and Gmail authorization; supports dry-run, draft, recipient controls, attachments, and HTML bodies.] <br>

## Skill Version(s): <br>
1.0.14 (source: ClawHub release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
