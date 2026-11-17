## Description:

Configure and troubleshoot OpenClaw model providers, routing, session model locks, cron model pinning, and provider switching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hohobohan](https://clawhub.ai/user/hohobohan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure OpenClaw model providers, verify active model routing, switch session models, and pin models for time-sensitive cron jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested OpenClaw configuration changes may affect API keys, provider URLs, default models, or cron model pins.

Mitigation: Review proposed openclaw.json edits and cron payload changes before applying them.

Risk: Existing sessions can remain locked to an older model after the default model changes.

Mitigation: Check the active session model and use an explicit /model switch or start a new session when the intended model must be used immediately.

Risk: Time-sensitive cron jobs can miss deadlines if they rely on a slow or cold-starting global default model.

Mitigation: Pin the model explicitly in cron payloads for scheduled jobs where delay matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hohobohan/skills/hobohan-model-config)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to OpenClaw configuration, provider settings, session model selection, cron payloads, and dmScope routing.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
