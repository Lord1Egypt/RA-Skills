## Description: <br>
Email outreach automation for importing CSV contacts, merging templates, sending personalized messages through SMTP, SendGrid, or Mailgun, and applying rate limits, unsubscribe language, and deliverability guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xianji520](https://clawhub.ai/user/xianji520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and growth teams use this skill to prepare and send small or bulk B2B outreach from a CSV contact list with templated personalization, provider selection, throttling, and send-result logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real outreach emails to recipients. <br>
Mitigation: Review recipient lists and rendered messages before sending, begin with a very small --max-per-run test, and keep rate limits conservative. <br>
Risk: Provider credentials or app passwords are required for SMTP, SendGrid, or Mailgun. <br>
Mitigation: Use limited app passwords or scoped ESP API keys, pass secrets through environment variables where supported, and avoid storing credentials in files. <br>
Risk: Bulk outreach can create compliance, unsubscribe, or deliverability issues. <br>
Mitigation: Send only to appropriate contacts, include unsubscribe or opt-out language, respect opt-out requests, and configure SPF, DKIM, and DMARC for the sending domain. <br>
Risk: The results CSV contains recipient data and delivery status. <br>
Mitigation: Protect the log file, restrict access to it, and delete it when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xianji520/outreach-pipeline) <br>
- [CSV Format](artifact/references/csv-format.md) <br>
- [Deliverability and Account Configuration Tips](artifact/references/tips.md) <br>
- [Compliance and Anti-Spam Tips](artifact/references/risks.md) <br>
- [First-Touch Template](artifact/assets/templates/first-touch.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, plain-text email templates, CSV inputs, and CSV send-result logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call SMTP, SendGrid, or Mailgun using user-provided credentials and writes per-recipient status results to a local CSV log.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
