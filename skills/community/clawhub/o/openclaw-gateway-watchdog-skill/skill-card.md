## Description:

Monitor the OpenClaw Gateway plus configured Spark, Local API Hub, and Dashboard loopback health endpoints with a read-only watchdog state machine, local state files, cooldown dedupe, and optional Discord alerts on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathanjing](https://clawhub.ai/user/jonathanjing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run foreground, cron, or macOS LaunchAgent watchdog checks for OpenClaw Gateway health and related local endpoints. It helps send low-noise Discord alerts for incidents and recoveries without rewriting OpenClaw configuration or restarting services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured Spark token can be sent to the configured Spark status URL, including a remote URL.

Mitigation: Keep SPARK_API_URL on a trusted loopback endpoint unless remote Spark access is intentional, and avoid automatic ~/.openclaw/.env token fallback for remote endpoints.

Risk: Cron or LaunchAgent setup creates recurring background checks and optional Discord notifications.

Mitigation: Enable cron or LaunchAgent mode only when recurring monitoring is desired, and use an allowlisted private Discord destination.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jonathanjing/skills/openclaw-gateway-watchdog-skill)
- [ClawHub homepage metadata](https://clawhub.ai/jonathanjing/openclaw-gateway-watchdog-skill)
- [Cron Agent Turn Template](references/cron-agent-turn.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local watchdog state files and Discord incident messages when the operator runs the bundled scripts.]

## Skill Version(s):

1.0.4 (source: server evidence, SKILL.md metadata, skill.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
