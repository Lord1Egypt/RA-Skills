## Description: <br>
Provides daily Gmail briefings by listing unread or urgent emails, summarizing priorities, drafting replies, and helping manage inbox filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deliverydriver](https://clawhub.ai/user/deliverydriver) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and individual email users use this skill to triage Gmail inboxes, review unread or urgent messages, summarize priorities, and prepare reply drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive mailbox access could expose private personal or work email. <br>
Mitigation: Grant access only to the intended mailbox, prefer narrow provider scopes, and use a separate profile for work or personal accounts. <br>
Risk: Email actions such as send, delete, reply, forward, or modify could affect the wrong account or message. <br>
Mitigation: Confirm the account, recipient or message ID, and exact action before performing any mailbox mutation. <br>


## Reference(s): <br>
- [GOG SOP](references/gog-sop.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and drafted email text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference mailbox account, message identifiers, sender filters, unread status, and suggested reply drafts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
