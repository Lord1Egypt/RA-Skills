## Description:

Automatically monitors OpenClaw model health, switches from an unstable primary model to a configured fallback, and attempts failback after stability returns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovmanth](https://clawhub.ai/user/bovmanth)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to keep agent traffic available by monitoring the default model, selecting configured fallback models, and restoring the primary model after it passes health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic failover can change OpenClaw model routing and restart the gateway.

Mitigation: Review the immutable release before installation, run a single check before loop mode, and enable automatic switching only where gateway restarts are acceptable.

Risk: Fallback selection can route requests to configured providers or models that are not approved for the deployment.

Mitigation: Confirm every fallback model and provider is acceptable for the data being processed, and set excludedProviders before running the guard.

Risk: Long-running daemon or systemd use can repeatedly alter routing as health checks pass or fail.

Mitigation: Tune failover and recovery thresholds, inspect the state and log files after test runs, and use daemon mode only after the behavior is reviewed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can update OpenClaw model routing, write state and log files, and restart the OpenClaw gateway when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
