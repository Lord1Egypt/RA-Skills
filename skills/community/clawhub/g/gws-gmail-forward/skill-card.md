## Description: <br>
Gmail: Forward a message to new recipients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and workspace administrators use this skill to prepare Gmail forwarding actions through the gws CLI, including recipient selection, optional notes, attachments, drafts, and dry runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forwarded messages and attachments can expose private email when recipients or options are chosen carelessly. <br>
Mitigation: Confirm the authenticated Gmail account, message ID, recipients, and attachment handling before sending; use --dry-run or --draft when review is needed. <br>
Risk: The skill depends on the locally installed gws CLI to perform Gmail actions. <br>
Mitigation: Install and use the skill only when the local gws CLI is already trusted and configured for the intended Gmail account. <br>


## Reference(s): <br>
- [Gws Gmail Forward on ClawHub](https://clawhub.ai/googleworkspace-bot/gws-gmail-forward) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recipient, attachment, draft, dry-run, and HTML-body options for the gws Gmail forwarding command.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
