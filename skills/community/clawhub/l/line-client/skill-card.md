## Description:

LINE messaging integration via the Chrome extension gateway for sending and reading messages, managing contacts, groups, profile settings, and reactions, and authenticating with QR code login using HMAC-signed API access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2manslkh](https://clawhub.ai/user/2manslkh)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to let an agent operate a LINE account through the Chrome extension gateway for messaging, contact and group management, profile and settings changes, and event polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad access to private messages, contacts, groups, profile settings, and session tokens.

Mitigation: Install only when intentionally granting LINE account access and require explicit confirmation before reading messages, sending or unsending messages, changing contacts or groups, issuing tokens, or modifying profile and settings.

Risk: Stored LINE tokens and certificate cache can expose account access if leaked through files, logs, or prompts.

Mitigation: Treat ~/.line-client/tokens.json and ~/.line-client/sqr_cert as secrets, restrict file permissions, and avoid sharing logs or prompts that reveal their contents.

Risk: QR login requires a time-sensitive user scan and PIN entry, so mishandled authentication can fail or expose login flow details.

Mitigation: Send the PIN only to the account owner over a trusted channel immediately after it is generated.

## Reference(s):

- [Line Client ClawHub listing](https://clawhub.ai/2manslkh/skills/line-client)
- [2manslkh publisher profile](https://clawhub.ai/user/2manslkh)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in LINE account operations through authenticated client methods.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
