## Description:

Email processing for Greek accounting. Connects via IMAP to scan for financial documents, AADE notices, and invoices. Routes to local pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto)

### License/Terms of Use:


## Use Case:

Developers and operators supporting Greek accounting workflows use this skill to configure and guide email scanning, document classification, and routing for invoices, bank statements, AADE/EFKA notices, and client inquiries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive accounting email and related attachments.

Mitigation: Confirm mailbox scopes and account boundaries before installation, use a dedicated service mailbox, prefer read-only IMAP for monitoring, and document where email content or summaries may leave the environment.

Risk: Outbound messages or forwarded attachments could expose sensitive information if enabled without controls.

Mitigation: Disable SMTP, Mail.Send, and Mail.ReadWrite unless explicitly needed, and require human review before any email is sent or attachment is forwarded.

Risk: Automatic reply behavior needs careful review because the security summary flags inconsistent guidance.

Mitigation: Treat all auto-responses as draft-only until a human approves the exact recipient, content, and attachments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/satoshistackalotto/skills/greek-email-processor)
- [Publisher profile](https://clawhub.ai/user/satoshistackalotto)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, YAML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Greek email templates, processing workflows, and configuration guidance; outbound email actions require human approval.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
