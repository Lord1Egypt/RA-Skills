## Description:

Generate and manage temporary disposable email addresses valid for 30 minutes to receive and retrieve verification emails and messages without authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zororaka00](https://clawhub.ai/user/zororaka00)

### License/Terms of Use:


## Use Case:

Developers and agents use Mailtap to create disposable email addresses for low-risk testing, poll temporary inboxes, and retrieve messages or attachments without using a personal email account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated temporary inboxes can expose verification emails or one-time links to public access.

Mitigation: Use only for low-risk testing or disposable workflows, never for password resets, financial accounts, identity checks, wallet recovery, privileged account creation, or similar access-granting flows.

Risk: Attachments retrieved from MailTap inboxes are public and untrusted.

Mitigation: Review attachment metadata before download, restrict file types and size, and download only into a controlled sandbox.

Risk: Automated handling of verification messages can create misuse risk when used outside authorized testing.

Mitigation: Use the skill only where temporary email automation is permitted and the target service workflow is authorized.

## Reference(s):

- [MailTap service](https://www.mailtap.org)
- [MailTap API root](https://api.mailtap.org)
- [Mailtap ClawHub listing](https://clawhub.ai/zororaka00/skills/mailtap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with JSON examples, HTTP endpoints, bash commands, and Python helper code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses are JSON; temporary email addresses expire after 30 minutes.]

## Skill Version(s):

1.0.4 (source: server release metadata and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
