## Description: <br>
Email processing for Greek accounting. Connects via IMAP to scan for financial documents, AADE notices, and invoices. Routes to local pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Greek accounting teams use this skill to process business email, identify invoices, bank statements, AADE and EFKA notices, and client payment inquiries, then route documents and draft responses for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read sensitive accounting emails and local documents, including invoices, tax notices, bank statements, and client records. <br>
Mitigation: Use a dedicated mailbox or app password, keep IMAP permissions as narrow as possible, and protect the configured local data directory. <br>
Risk: Optional outbound email, calendar, and notification integrations can disclose information or send messages unintentionally if enabled without review. <br>
Mitigation: Enable only required integrations, keep SMTP and Mail.Send disabled unless needed, and require human approval before any outbound response. <br>
Risk: The security review marked the release suspicious because it handles sensitive email workflows and has inconsistent integration and approval guidance. <br>
Mitigation: Review configuration before installation, verify external integrations are intentionally configured, and inspect generated drafts and routing actions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/satoshistackalotto/greek-email-processor) <br>
- [Project homepage from artifact metadata](https://github.com/satoshistackalotto/openclaw-greek-accounting) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, YAML-style configuration examples, response templates, and processing workflow summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq, curl, OPENCLAW_DATA_DIR, IMAP_HOST, IMAP_USER, and IMAP_PASSWORD; SMTP, Gmail API, Microsoft Graph, Google Calendar, and Slack settings are optional.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
