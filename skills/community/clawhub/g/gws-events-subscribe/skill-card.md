## Description:

Google Workspace Events: Subscribe to Workspace events and stream them as NDJSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to have an agent prepare Google Workspace event subscription commands, including target resources, event types, Pub/Sub subscription options, polling behavior, cleanup, and optional event file output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gws CLI and referenced shared authentication rules are external prerequisites that affect access to Google Workspace and GCP resources.

Mitigation: Before installing or using the skill, confirm trust in the gws CLI and review the shared authentication rules.

Risk: Event subscription commands can create or reuse Pub/Sub resources and may leave resources persistent when cleanup is not selected.

Mitigation: Use the narrowest required Google Workspace and GCP permissions, and choose --cleanup when persistent Pub/Sub resources are not wanted.

Risk: Writing event payloads to a local output directory can store sensitive workspace data.

Mitigation: Treat local event output as sensitive data and restrict where output files are written and retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-events-subscribe)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Google Workspace resource URIs, CloudEvents type lists, GCP project IDs, Pub/Sub subscription names, polling options, cleanup options, acknowledgement behavior, and local output directory settings.]

## Skill Version(s):

1.0.12 (source: server release metadata); artifact metadata version 0.22.5

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
