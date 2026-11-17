## Description:

H-ear helps agents classify environmental audio from URLs, local files, and RTSP captures, then report sound events, supported classes, jobs, usage, and webhook activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[badajoz95](https://clawhub.ai/user/badajoz95)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external teams use this skill to add H-ear audio classification and monitoring workflows to agent channels such as WhatsApp, Telegram, Slack, Discord, and Teams. It supports class lookup, usage and job inspection, audio classification, webhook callbacks, reports, waveform links, and RTSP capture-assisted classification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RTSP capture/listen can record from a camera source and uploads captured audio for classification by default.

Mitigation: Use capture/listen only with explicit operator intent, avoid credentials in RTSP URLs, and pass --no-classify when recording should not be uploaded.

Risk: Webhook create, update, and delete commands change persistent enterprise integrations and may expose webhook URLs, delivery history, or a one-time signing secret.

Mitigation: Limit webhook operations to authorized operators, confirm IDs and target URLs before changes, and handle signing secrets as sensitive values.

Risk: Audio files, URLs, local recordings, location metadata, and webhook payloads may be sent to H-ear services.

Mitigation: Confirm users are permitted to share those data types with H-ear before use.

## Reference(s):

- [H-ear World](https://h-ear.world)
- [ClawHub skill page](https://clawhub.ai/badajoz95/skills/h-ear)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text returned by CLI/API-backed commands, with JSON available for tool introspection.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires H-ear credentials and may return SAS audio/report URLs or webhook metadata depending on command.]

## Skill Version(s):

1.1.8 (source: server release evidence, created 2026-04-30; artifact manifests report 1.1.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
