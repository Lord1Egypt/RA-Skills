## Description:

Three-agent pipeline orchestrator (Kalshalyst, Eval, Executor) for automated Kalshi prediction market trading with validation loops and retry logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingmadellc](https://clawhub.ai/user/kingmadellc)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and prediction-market operators use this skill to coordinate Kalshi market intake, estimation, validation, sizing, execution, and status reporting for the OpenClaw stack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct live Kalshi trading activity.

Mitigation: Use paper trading during setup and require manual confirmation before any live order.

Risk: The bundled monitor may expose local process, config, and log data without authentication.

Mitigation: Bind the monitor to 127.0.0.1, add authentication, remove wildcard CORS, and redact process, config, and log endpoints before network exposure.

Risk: Credentials or sensitive configuration values may be exposed through logs or browser-served configuration data.

Mitigation: Keep credentials out of logs and served configuration values; redact or disable sensitive endpoints before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingmadellc/skills/prediction-stack-orchestrator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON logs, markdown reports, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce trade execution instructions and monitor status outputs; users should confirm live orders before execution.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
