## Description: <br>
Aggregates notification email from services such as GitHub, Stripe, and Linear into a ClawHub notify mailbox, immediately forwards urgent messages, and sends lower-priority items as a daily digest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1458428190](https://clawhub.ai/user/1458428190) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to centralize SaaS notification email, route urgent payment, CI, security, outage, and deployment alerts immediately, and receive routine notifications as a daily Markdown digest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The notification routing scripts can execute unsafe shell commands from attacker-controlled email subject text. <br>
Mitigation: Do not enable scheduled polling until command execution is changed to execFileSync or spawn with argument arrays, the unpinned npx fallback is removed, and testing is performed with --dry-run and a dedicated low-privilege notify mailbox. <br>
Risk: Digest logs are written to a shared temporary directory and may expose notification metadata. <br>
Mitigation: Store digest logs in a private user directory with explicit retention before enabling unattended use. <br>


## Reference(s): <br>
- [notify-hub ClawHub release](https://clawhub.ai/1458428190/notify-hub) <br>
- [Publisher profile](https://clawhub.ai/user/1458428190) <br>
- [clawEmail console](https://claw.163.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, forwarded notification email, and daily digest email] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mail-cli with a notify profile; supports dry-run checks before sending or marking mail as read.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
