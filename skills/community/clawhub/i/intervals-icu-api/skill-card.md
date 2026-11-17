## Description:

Complete guide for accessing and managing training data with the intervals.icu API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pseuss](https://clawhub.ai/user/pseuss)

### License/Terms of Use:


## Use Case:

Developers, coaches, and athletes use this skill to retrieve Intervals.icu training activities, manage planned workouts and calendar events, log wellness data, and generate credentialed API requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes live credentialed POST, PUT, bulk, hide/lock, sport-setting, wellness, and DELETE operations that can change an Intervals.icu account.

Mitigation: List and verify target records first, confirm athlete and event IDs, and keep a backup or export before destructive or bulk actions.

Risk: API keys and OAuth tokens may be exposed through chat transcripts, shell history, screenshots, or saved scripts.

Mitigation: Keep credentials out of shared text and persisted command history where possible, and use placeholders or secure secret handling for examples.

Risk: The server security verdict is suspicious because the guide documents live account changes without clear safety guidance.

Mitigation: Review the skill before use with a real Intervals.icu account and treat write operations as account-changing actions requiring confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pseuss/skills/intervals-icu-api)
- [Intervals.icu settings](https://intervals.icu/settings)
- [Intervals.icu API base URL](https://intervals.icu/api/v1)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes credentialed curl examples for read, write, bulk update, export, and delete-capable Intervals.icu operations.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
