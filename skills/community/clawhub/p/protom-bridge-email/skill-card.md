## Description:

Send email through Proton Mail Bridge (localhost SMTP) using age-encrypted credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boilerrat](https://clawhub.ai/user/boilerrat)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to set up Proton Mail Bridge credentials for an agent mailbox and send automated email such as daily reports or alerts through local SMTP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sender decrypts Proton Bridge credentials and can access outgoing email content.

Mitigation: Review scripts/send_email.py before automated use, restrict access to the age identity and encrypted env file, and use only dedicated Bridge credentials for the agent mailbox.

Risk: Non-local or unencrypted SMTP settings could expose credentials or route mail through an unintended server.

Mitigation: Keep SMTP_HOST set to 127.0.0.1 or another verified loopback address and avoid SMTP_SECURITY=NONE.

Risk: Temporary plaintext env files can expose Proton Bridge secrets if left on disk.

Mitigation: Encrypt the env file promptly with scripts/encrypt_env.sh and remove temporary plaintext copies immediately.

## Reference(s):

- [Proton Mail Bridge setup](references/proton-bridge-setup.md)
- [Proton Mail Bridge](https://proton.me/mail/bridge)
- [ClawHub skill page](https://clawhub.ai/boilerrat/skills/protom-bridge-email)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local setup guidance and commands; sending mail requires Proton Bridge, age, encrypted credentials, and local SMTP access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
