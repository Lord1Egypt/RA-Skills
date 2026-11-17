## Description:

OpenClaw Guardian CN helps an agent monitor OpenClaw Gateway health, run scheduled self-checks, and propose or execute recovery commands when common service issues are detected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenbinxin](https://clawhub.ai/user/shenbinxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check OpenClaw Gateway status, configure periodic watchdog checks, review OpenClaw skill and channel health, and recover from stopped or disconnected Gateway processes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can configure persistent cron or Scheduled Task watchdogs.

Mitigation: Review each scheduled entry before enabling it and keep a documented command for disabling the watchdog.

Risk: Recovery behavior can restart OpenClaw Gateway services without clear user opt-in.

Mitigation: Require explicit operator approval before enabling automatic recovery or service restart behavior.

Risk: The artifact includes an eval-based recovery example.

Mitigation: Remove or replace eval usage with an allowlisted command dispatcher before deployment.

Risk: Some state and log files are written under /tmp.

Mitigation: Move persistent state and logs to an access-controlled OpenClaw data directory.

Risk: Windows examples use RunLevel Highest for scheduled tasks.

Mitigation: Avoid elevated scheduled task privileges unless the deployment requires them and the command has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenbinxin/skills/openclaw-guardian-cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status reports with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scheduled task or cron instructions and recovery command results.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
