## Description: <br>
MailerSend (mailersend.com). Use this skill for ANY MailerSend request, including reading, creating, and updating data through the OOMOL MailerSend connector instead of direct API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to inspect MailerSend connector schemas, list or retrieve MailerSend resources, and send transactional email from a connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected MailerSend account and may use sensitive credentials through the OOMOL connector. <br>
Mitigation: Review requested account access before use and rely on the connector-managed credential flow rather than handling raw API tokens. <br>
Risk: The send_email action can send transactional email and change external system state. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-mailersend) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [MailerSend homepage](https://www.mailersend.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce oo CLI commands that call MailerSend connector actions and return JSON responses from the connector.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
