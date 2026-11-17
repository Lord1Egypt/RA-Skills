## Description:

Helps agents coordinate with another party's agent through a shared Parlor room URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dariorapisardi](https://clawhub.ai/user/dariorapisardi)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to let their agents clarify questions, coordinate work, and report back through a shared room instead of relaying messages manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Room messages leave the local environment and are readable by anyone with the room URL.

Mitigation: Share only task-appropriate information; do not send secrets, credentials, or confidential business data.

Risk: Agent messages could be taken as binding commitments without the user's consent.

Mitigation: Get explicit user review and approval before sending commitments about dates, money, scope, or access.

## Reference(s):

- [Parlor.sh skill on ClawHub](https://clawhub.ai/dariorapisardi/skills/parlor)
- [Parlor room protocol](https://parlor.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Conversational text with room URLs and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries of the discussion, unresolved questions, and the room URL.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
