## Description:

Splits long outgoing agent messages into smaller ordered chunks to avoid channel truncation or delivery failure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[54meteor](https://clawhub.ai/user/54meteor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep long responses deliverable in chat channels with per-message length limits by splitting text into ordered chunks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long replies may be divided into multiple messages and include ordered chunk markers.

Mitigation: Review split output for completeness and ordering when using channels with strict message length limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/54meteor/skills/message-split)
- [ClawHub publisher profile](https://clawhub.ai/user/54meteor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Text or Markdown split into sequentially labeled message chunks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adds ordered chunk markers when a response is split.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
