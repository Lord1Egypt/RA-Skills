## Description:

Provides daily or periodic Gmail briefings by listing unread and urgent emails, summarizing priorities, drafting replies, and supporting inbox flagging or archiving workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deliverydriver](https://clawhub.ai/user/deliverydriver)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users use this skill to triage Gmail inboxes, identify priority unread messages, and prepare draft replies for review. It is intended for authenticated Gmail or GOG CLI setups where the user wants periodic inbox digests and sender-focused filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an authenticated Gmail or GOG setup to inspect unread mailbox content.

Mitigation: Install it only for accounts where Gmail triage is intended and where mailbox access has been approved by the account owner.

Risk: Draft replies, archive actions, or flagging changes could affect real email workflows if applied without review.

Mitigation: Review any proposed draft, archive, or flagging action before allowing the agent to change the mailbox.

Risk: The bundled SOP contains a personal Gmail address.

Mitigation: Replace the embedded address with the user's own account or a neutral configuration placeholder before use.

## Reference(s):

- [GOG SOP](references/gog-sop.md)
- [ClawHub Skill Page](https://clawhub.ai/deliverydriver/skills/gmail-briefings)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with inline shell commands and draft reply text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires review before draft replies, archive actions, or flagging changes are applied to the mailbox.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
