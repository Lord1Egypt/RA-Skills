## Description:

A comprehensive AI agent skill for managing incoming messages across email, chat, and other communication channels by triaging urgency, drafting replies, tracking threads, reducing notification noise, and producing a daily communication overview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ethagent](https://clawhub.ai/user/ethagent)

### License/Terms of Use:


## Use Case:

External users use this skill to triage incoming communications across connected email, chat, and messaging channels, draft replies for approval, track follow-ups, reduce notification noise, and review communication patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill aggregates and profiles sensitive communications across email, chat, and other messaging channels.

Mitigation: Connect only accounts and channels the user is comfortable having analyzed, and prefer controls that exclude sensitive contacts or channels.

Risk: The skill reads sent messages and relationship context to draft replies in the user's voice.

Mitigation: Require review and explicit approval of the exact outgoing text before any message is sent.

Risk: The security evidence notes limited scoping and retention controls for communication history and cross-channel mappings.

Mitigation: Limit message history where possible and look for controls to delete stored profiles, relationship context, and cross-channel mappings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ethagent/skills/messages)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text summaries with draft message content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft replies, follow-ups, unsubscribe, mute, and clearing actions require user confirmation before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
