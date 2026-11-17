## Description:

MoltMail-powered Web3 email skill that lets agents create or access a wallet-backed inbox to send, receive, read, and manage mail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tempepeot](https://clawhub.ai/user/tempepeot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent a MoltMail/EtherMail inbox for disposable email, mailbox management, sending replies, account confirmations, and wallet-backed email workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet and mailbox credentials and persists encrypted wallet configuration and auth tokens locally.

Mitigation: Use it only with MoltMail/EtherMail accounts you trust, avoid importing a valuable wallet private key, and protect the local state directory.

Risk: The passphrase can be supplied through an environment variable on shared systems.

Mitigation: Prefer interactive passphrase entry when other users or processes may inspect the environment.

Risk: The security summary reports dependency versions flagged for security issues.

Mitigation: Update dependencies and rerun security checks before using the skill for sensitive mail or account workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tempepeot/skills/moltmailermp)
- [MoltMail homepage](https://moltmail.io)
- [EtherMail homepage](https://ethermail.io)
- [OpenClaw homepage](https://openclaw.ai)
- [Declared source repository](https://github.com/EtherMailOrg/moltmail-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with npm shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces mailbox, message, alias, referral, reward, setup, login, send, and reply guidance through local npm scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
