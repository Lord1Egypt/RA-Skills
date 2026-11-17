## Description:

Predict satellite passes for NOAA APT, METEOR LRPT, and ISS targets at a configured location, then send WhatsApp alerts with manual dish alignment details and optional capture/decode orchestration hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davestarling](https://clawhub.ai/user/davestarling)

### License/Terms of Use:

MIT

## Use Case:

Developers and SDR operators use this skill to configure and run a zero-AI satellite pass scheduler for reception planning, WhatsApp pass alerts, and optional downstream capture/decode automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured capture or decode hooks can run shell commands automatically from scheduled execution.

Mitigation: Keep hooks disabled until each command is written and reviewed by the operator, and run the scheduler under a low-privilege account.

Risk: Scheduled command execution may inherit environment variables from the process.

Mitigation: Avoid placing secrets in the cron or scheduler environment and use narrowly scoped credentials for notification and remote host access.

## Reference(s):

- [Satellite Copilot ClawHub release](https://clawhub.ai/davestarling/skills/moltbot-satellite-copilot)
- [README](artifact/README.md)
- [Example configuration](artifact/config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scheduler setup steps, configuration edits, cron commands, and operational guidance for satellite pass alerts.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
