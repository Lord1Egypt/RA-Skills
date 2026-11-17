## Description:

Triage Gmail into spam, informational, and action-required lanes, propose cleanup and reply drafts, and apply mailbox changes only after owner approval through Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyang001](https://clawhub.ai/user/joeyang001)

### License/Terms of Use:

MIT-0

## Use Case:

Gmail account owners use this skill to review grouped inbox triage on Telegram, approve proposed archiving or trashing, and prepare replies without automatically sending them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access to sensitive Gmail messages and credentials may expose private information.

Mitigation: Use a narrowly scoped Gmail query, supply the keyring password only for the run through a secret manager, and send digests only to the configured Telegram owner.

Risk: Incorrect classification or overly broad approval could archive or trash important messages.

Mitigation: Review pending and approved actions, leave dry-run enabled until reviewed, and keep the per-run action cap modest.

Risk: A reply draft could be sent without the owner's intent if send permissions are loosened.

Mitigation: Keep the send gate enabled and require explicit owner approval for each send.

## Reference(s):

- [Gmail Cleanup on ClawHub](https://clawhub.ai/joeyang001/skills/gmail-cleanup)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Telegram digest, JSON action proposals and reply drafts, and execution audit log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mailbox changes require an approved action list; sending drafts requires separate authorization.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
