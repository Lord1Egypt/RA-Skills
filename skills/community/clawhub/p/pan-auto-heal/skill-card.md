## Description:

Auto-Heal 通用守护 monitors HTTP, port, process, and command checks, then runs configured repair or rollback commands and logs alerts when services stay unhealthy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panjun2026](https://clawhub.ai/user/panjun2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to configure an agent-assisted service guard that checks service health, attempts repairs, rolls back when configured, and records alerts for manual intervention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured health-check, repair, and rollback commands can execute arbitrary or privileged shell commands.

Mitigation: Review every services.json command as trusted code before use and run the guard under the least-privileged account that can perform the needed action.

Risk: Untrusted changes to the configuration file or its parent directory could alter unattended repair behavior.

Mitigation: Protect services.json and its parent directory from untrusted writes.

Risk: Command strings may expose credentials or other secrets.

Mitigation: Avoid plaintext secrets in command strings and move sensitive values to protected secret-management paths where possible.

Risk: Repeated unattended restarts or rollbacks can amplify an incident.

Mitigation: Test manually before enabling cron, and add rate limits or alerting around repeated repair attempts.

## Reference(s):

- [Auto-Heal 配置示例](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/panjun2026/skills/pan-auto-heal)
- [Publisher profile](https://clawhub.ai/user/panjun2026)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational run instructions and configuration patterns for service health checks, repair commands, rollback commands, logging, and cron scheduling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
