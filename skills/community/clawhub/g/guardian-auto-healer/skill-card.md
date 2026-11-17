## Description:

OpenClaw 7x24 watchdog & auto-healer. Monitors gateway health, memory usage, zombie sessions, and disk space every 5 minutes with automatic restart when stuck.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install a recurring watchdog that checks gateway health, memory usage, and disk space and restarts the gateway when it is unresponsive or above the kill threshold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent recurring automation can repeatedly execute the watchdog and restart the OpenClaw gateway.

Mitigation: Enable it only when continuous auto-healing is intended, test a manual run first, and confirm the cron job can be disabled or removed.

Risk: The watchdog depends on local script paths, process matching, restart thresholds, and log paths that may not fit every environment.

Mitigation: Review and harden the script path, process matching, thresholds, and log location before scheduling the recurring job.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/openlark/skills/guardian-auto-healer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON cron configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and operations guidance for a persistent watchdog script and recurring cron-style agent job.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
