## Description: <br>
Lel Mail helps an agent read unread mailbox messages, queue outgoing email, manage pending email, and act on received email through Python and shell scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Leli1024](https://clawhub.ai/user/Leli1024) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and agent operators use this skill to connect an agent to a configured mailbox, check unread messages, schedule outbound email, and inspect or delete queued outgoing mail. It is best suited for environments where email credentials and account permissions can be tightly controlled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incoming emails can steer agent actions, including memory writes, user contact, and delayed outbound email. <br>
Mitigation: Keep can_read and can_send disabled unless needed, use a dedicated mailbox or scoped app password, and require manual approval before email-derived memory writes, user contact, or outgoing responses. <br>
Risk: The local email configuration stores mailbox credentials and account permissions. <br>
Mitigation: Protect ~/.config/lel-mail/config.json, avoid shared accounts, and review account permissions before enabling mailbox access. <br>
Risk: Queued outgoing mail may be sent later by the cron-driven sender. <br>
Mitigation: Review the queue with manage_queue.py before enabling the sender daemon and delete unintended messages before they are sent. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Leli1024/lel-mail) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with shell commands and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON configuration and queue files under ~/.config/lel-mail when installed and run.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
