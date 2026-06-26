## Description: <br>
Email sending skill via SMTP or API providers. Supports attachments, HTML templates, and batch sending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and trigger SMTP or email-provider sends, including HTML messages, attachments, and batch recipient workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential-backed email sending can transmit messages, attachments, or batches to unintended recipients. <br>
Mitigation: Use tightly scoped email-provider credentials and require explicit preview and approval of every recipient list, attachment, subject, body, and batch send before transmission. <br>
Risk: The release evidence flags broad email-sending capability without enough user-control safeguards. <br>
Mitigation: Review the send_email.py implementation before installation and run the skill only in workflows with clear human approval gates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-email-sender) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jpengcheng523-netizen) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can describe provider credentials, recipient inputs, attachments, HTML templates, and batch sending options.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
