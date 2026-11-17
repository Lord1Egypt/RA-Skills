## Description:

Full read/write Zoho Mail access for OpenClaw agents

This skill is ready for commercial/non-commercial use.

## Publisher:

[panthrocorp](https://clawhub.ai/user/panthrocorp)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators and agents use this skill to configure and authenticate Zoho Mail access, then list, read, search, send, reply to, delete, and mark messages in an EU-region Zoho Mail account.

### Deployment Geography for Use:

Europe (Zoho EU data centre)

## Known Risks and Mitigations:

Risk: Delegating full read/write Zoho Mail access can expose sensitive mail and allow send, reply, delete, and mark actions.

Mitigation: Install only for operators who intend to grant full mailbox control, and restrict who can invoke send and delete commands.

Risk: Installing a mutable remote binary without integrity verification can install an unexpected artifact.

Mitigation: Pin the release and verify a reviewed checksum or signature before installing.

Risk: OAuth tokens, token encryption keys, and pasted OAuth redirect URLs are sensitive.

Mitigation: Protect ZOHO_MAIL_TOKEN_KEY and the token directory, avoid logging redirect URLs, and revoke the Zoho session when access is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/panthrocorp/skills/panthrocorp-zoho-mail)
- [Project Homepage](https://github.com/PanthroCorp-Limited/openclaw-skills)
- [Zoho API Console (EU)](https://api-console.zoho.eu/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Zoho OAuth credentials and ZOHO_MAIL_TOKEN_KEY; write-capable commands can send, reply to, delete, and mark mail.]

## Skill Version(s):

0.3.1 (source: server release metadata, CHANGELOG, dist/metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
