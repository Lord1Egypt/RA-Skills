## Description:

Learns and adapts to the user's personality over time by observing communication style, values, decision-making patterns, and preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enjuguna](https://clawhub.ai/user/enjuguna)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help an agent maintain a local personality profile, collect observation logs, and adapt response behavior to a user's stated and inferred preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists a named user's personality profile and conversation-derived observations.

Mitigation: Remove the shipped profile and observations before use, obtain user consent, and define correction and deletion procedures.

Risk: The observation workflow scans private local memory and assistant logs.

Mitigation: Restrict scanning to user-approved files and run dry-run reviews before enabling scheduled collection.

Risk: Scheduled observation and adaptation can create durable profiling without ongoing review.

Mitigation: Avoid cron or other automation until consent, review controls, retention limits, and audit procedures are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enjuguna/skills/personality-adapt)
- [Publisher profile](https://clawhub.ai/user/enjuguna)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and local profile/configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces durable local personality observations and updates to profile files.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
