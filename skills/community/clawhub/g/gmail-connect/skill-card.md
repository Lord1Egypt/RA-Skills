## Description:

Connects OpenClaw to Gmail on Ubuntu through a local OAuth wizard to search and read mail, check for new messages, and optionally send user-reviewed drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[svetlyoh](https://clawhub.ai/user/svetlyoh)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers on Ubuntu use this skill to connect a Gmail account, find and read messages, check inbox activity, and prepare drafts for optional review and sending in a local browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth credentials, tokens, cached mail metadata, and drafts are stored in unencrypted local files.

Mitigation: Protect the Ubuntu account and owner-only state directory; never share credential files or tokens in chat.

Risk: The private wizard link and optional send permission can expose account access or enable unintended email delivery.

Mitigation: Keep the wizard link private, leave sending disabled unless needed, and review each message before sending.

Risk: Optional background checks create a persistent Gmail polling service.

Mitigation: Enable background checks only when wanted; stop the user-level service when no longer needed.

## Reference(s):

- [ClawHub release](https://clawhub.ai/svetlyoh/skills/gmail-connect)
- [Project homepage (listed metadata; import provenance unavailable)](https://github.com/svetlyoh/web-wallet/tree/master/openclaw/skills/gmail-connect/gmail-connect)
- [Operations and setup](references/operations.md)
- [Privacy and local data handling](PRIVACY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown responses with email summaries and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local drafts require explicit user review in the browser before sending.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; bundled frontmatter says 0.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
