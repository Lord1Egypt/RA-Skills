## Description: <br>
Gmail automation: summarize, labels, spam purge, filing, deletion, permanent delete <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[r39132](https://clawhub.ai/user/r39132) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and agents use this skill to inspect Gmail inbox state, summarize unread mail, manage labels, move messages, and run spam, trash, and old-message cleanup tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run persistent mailbox-changing jobs that continue outside the agent session. <br>
Mitigation: Review each requested background job before launch, verify the Gmail account and WhatsApp notification target, and monitor job status until completion. <br>
Risk: Some workflows can trash or permanently delete Gmail messages. <br>
Mitigation: Use destructive actions only after explicit confirmation, avoid full-scope authorization unless permanent deletion is required, and prefer trash-based deletion when possible. <br>
Risk: Raw Gmail task status and results may be sent to a configured WhatsApp recipient. <br>
Mitigation: Confirm the recipient before execution and avoid sending sensitive mailbox contents through notification channels. <br>
Risk: The background command wrapper executes a constructed command string. <br>
Mitigation: Use only the documented Gmail helper commands and avoid untrusted labels, dates, or command text in background jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/r39132/gmail-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch background Gmail maintenance jobs and report status or results through configured WhatsApp notifications.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
