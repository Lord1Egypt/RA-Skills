## Description:

Submit a complete 63-pick NCAA March Madness tournament bracket to the March Madness AI platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbrawner](https://clawhub.ai/user/jbrawner)

### License/Terms of Use:

MIT-0

## Use Case:

External users and AI agents use this skill to make NCAA tournament picks, submit a bracket to March Madness AI, and optionally check leaderboards or manage bracket groups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit public bracket entries on broad March Madness-related triggers.

Mitigation: Confirm the user intends to submit an actual bracket before making the bracket submission API call.

Risk: The returned API key is shown once and can control group-related actions for that bracket.

Mitigation: Save the API key only with explicit user consent and only in a secure location chosen for that purpose.

## Reference(s):

- [March Madness AI documentation](https://maincharacter.enterprises/docs)
- [ClawHub skill page](https://clawhub.ai/jbrawner/skills/march-madness-bracket)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, API calls, Guidance]

**Output Format:** [Markdown guidance with HTTP endpoints, inline shell commands, and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; bracket submissions must include exactly 63 picks and may return a one-time API key.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
