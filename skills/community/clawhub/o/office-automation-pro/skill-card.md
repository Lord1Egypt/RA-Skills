## Description: <br>
Automates common office workflows, including document processing, data organization, email management, scheduling, and report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wensen2024](https://clawhub.ai/user/wensen2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and office teams use this skill to automate routine HR, finance, sales, administrative, and operations workflows such as generating documents, cleaning spreadsheets, sending template-based email, scheduling meetings, and producing recurring reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad access to sensitive office files, including HR, finance, customer, and database-derived content. <br>
Mitigation: Back up files before batch operations, limit the working set to the minimum required documents, and require explicit approval before processing sensitive content. <br>
Risk: The skill can send emails and distribute generated reports, which may expose confidential information if recipients or templates are wrong. <br>
Mitigation: Require explicit approval before sending emails or distributing reports, and review recipients, attachments, and generated content before release. <br>
Risk: Optional SMTP configuration may expose mailbox credentials if long-lived passwords are stored in configuration files. <br>
Mitigation: Use a limited mailbox or app password and avoid storing SMTP passwords in reusable configuration files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wensen2024/office-automation-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text reports, generated office files, and optional JSON email configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, transform, generate, or distribute office documents and email content based on user-supplied files and configuration.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter and artifact changelog list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
