## Description:

Lobster Says is an OpenClaw companion skill that helps users set up a personalized emotional-support companion, schedules daily IM check-ins, and can use a user-selected memory mode to summarize local conversation transcripts through nixiashuo.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaredwei01](https://clawhub.ai/user/jaredwei01)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to initialize and manage a scheduled emotional-support companion that sends daily messages, studio links, screenshots, and optional memory-based summaries. It is intended for users who want recurring IM check-ins with explicit control over transcript processing modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists messaging jobs and may continue sending scheduled messages after setup.

Mitigation: Review registered OpenClaw cron jobs and pause or remove Lobster Says jobs when scheduled delivery is no longer desired.

Risk: Smart and deep memory modes can process private local OpenClaw transcripts, with deep mode sending raw transcript content to the service.

Mitigation: Choose lightweight mode to avoid transcript reading, or explicitly confirm smart/deep mode only when that data use is acceptable.

Risk: .lobster-config stores user identity, channel preferences, and access tokens used for service calls.

Mitigation: Treat .lobster-config and backups as secrets, limit filesystem access, and avoid sharing logs or archives that include the file.

Risk: Delivery behavior depends on correctly identifying group versus private IM targets, especially for WeCom.

Mitigation: Verify the configured delivery target before enabling scheduled messages and re-run setup from the intended IM conversation if target metadata is missing.

Risk: The skill depends on a remote nixiashuo.com service for generation, memory, delivery reporting, studio links, and screenshots.

Mitigation: Confirm the configured API host remains the intended service and expect related features to degrade if the service is unavailable.

## Reference(s):

- [Lobster Says ClawHub page](https://clawhub.ai/jaredwei01/skills/lobster-says)
- [nixiashuo.com service](https://nixiashuo.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational text and Markdown with inline shell commands, plus JSON or plain-text output from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scheduled IM message text, short-lived studio links, screenshot links or images, status summaries, and local configuration updates.]

## Skill Version(s):

2.5.8 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
