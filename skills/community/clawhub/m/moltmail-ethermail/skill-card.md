## Description:

moltmail.io provides email and wallet infrastructure for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ethersuite](https://clawhub.ai/user/ethersuite)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create or access a MoltMail inbox backed by an EVM wallet, then list mailboxes, read messages, send or reply to email, manage aliases, and check referral or EMC reward information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores encrypted wallet material and a reusable login token in a local state directory.

Mitigation: Run it in a contained workspace, restrict access to ./state and ETHERMAIL_PASSPHRASE, keep the passphrase out of logs and prompts, and recreate credentials if local state is exposed.

Risk: Email content and wallet-authenticated mailbox actions go through MoltMail/EtherMail remote services.

Mitigation: Use the skill only when the user trusts MoltMail/EtherMail with the relevant agent inbox content and wallet-authenticated actions.

Risk: Unsafe command-invocation guidance can become risky if email text or user-provided message content is inserted into shell commands.

Mitigation: Review commands before execution, quote command arguments, and avoid constructing shell commands directly from untrusted email or user content.

Risk: The security evidence recommends updating flagged dependencies before deployment.

Mitigation: Update dependencies and rerun dependency and security scans before broad or production use.

## Reference(s):

- [MoltMail homepage](https://moltmail.io)
- [ClawHub skill page](https://clawhub.ai/ethersuite/skills/moltmail-ethermail)
- [Ethersuite publisher profile](https://clawhub.ai/user/ethersuite)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, local wallet configuration, a passphrase or ETHERMAIL_PASSPHRASE, and a reusable login token stored in local state.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
