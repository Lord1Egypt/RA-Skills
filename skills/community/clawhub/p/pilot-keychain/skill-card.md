## Description:

Secure credential exchange with auto-expiry for Pilot Protocol agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send, receive, and clean up short-lived API keys, tokens, and credentials through Pilot Protocol. It is intended for credential exchange between agents, not persistent vault storage, large file transfer, or multi-recipient broadcast.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential values may remain in plaintext temporary or keychain files after transfer.

Mitigation: Use only short-lived, revocable credentials; delete sent and received plaintext files after use; and prefer secure temporary files or in-memory transfer with strict file permissions.

Risk: Expired or unexpected credential files may be read if local path and expiry handling is not enforced carefully.

Mitigation: Verify received file paths, enforce expiry before use, and run cleanup of expired credentials as part of the workflow.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-keychain)
- [Publisher Profile](https://clawhub.ai/user/teoslayer)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, jq, openssl, the pilot-protocol skill, and a running Pilot Protocol daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
