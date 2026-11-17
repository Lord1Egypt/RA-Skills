## Description:

Operates the Message-in-a-Bottle (MIAB) LIFO callback stack for local agent ensembles, helping agents register wake paths and create, forward, return, resolve, inspect, and reap file-based callbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albzhu](https://clawhub.ai/user/albzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of trusted single-user ClawHub or OpenClaw agent ensembles use this skill to coordinate asynchronous delegation without polling. It provides command guidance and broker tooling for routing wake events, managing callback state, and cleaning up stale work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Callback task, summary, result, and resume content is persisted in local state and may be copied into messages sent to agents.

Mitigation: Do not place secrets or sensitive values in callback fields; reference locations only when necessary and keep $CLAW_HOME private.

Risk: Local agents can change wake routing without strong actor authentication.

Mitigation: Install only for a trusted single-user agent ensemble and restrict who can run the CLI or modify $CLAW_HOME.

Risk: Administrative overrides and outside resume files can bypass normal safety boundaries.

Mitigation: Review uses of --force, --allow-outside, register, and --session-key before operation and keep an audit trail of intentional overrides.

Risk: A scheduled reaper can fail legitimate long-running callbacks if the TTL is too short.

Mitigation: Run the reaper in dry-run mode first, review callback-reaper.log, and set a TTL that matches the deployment's workload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albzhu/skills/miab-broker)
- [Publisher profile](https://clawhub.ai/user/albzhu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with inline shell commands and JSON-oriented command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for local file-backed callback state; command output can include dispatch messages, next steps, warnings, and status JSON.]

## Skill Version(s):

2.0.0 (source: release evidence and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
