## Description:

Self-healing watchdog for OpenClaw gateway that backs up openclaw.json, health-checks the gateway process, and rolls back to the last known good config on failure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and inspect a persistent OpenClaw gateway watchdog that backs up configuration, checks service health, restarts failed processes, and rolls back to a known-good config when recovery is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent scheduled execution for an OpenClaw gateway watchdog.

Mitigation: Install only when persistent self-healing behavior is intended, and review scheduled jobs before enabling them.

Risk: The security guidance flags broad cron removal that could affect unrelated cron entries.

Mitigation: Back up the current crontab and replace broad removal patterns with exact markers for this watchdog job.

Risk: The security guidance flags root-service examples and permissive handling of watchdog scripts and config backups.

Mitigation: Run the watchdog as an unprivileged user where possible and set restrictive permissions on the watchdog script and OpenClaw config backups.

Risk: Repeated failures can trigger repeated config rollback or log growth.

Mitigation: Add retry and retention limits so transient failures do not repeatedly roll back configuration or fill disk.

## Reference(s):

- [Docker Self-Healing Setup](references/docker.md)
- [macOS LaunchDaemon](references/launchd.md)
- [Systemd Service](references/systemd.md)
- [ClawHub Skill Page](https://clawhub.ai/mupengi-bot/skills/gw-self-heal)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with bash, Dockerfile, launchd plist, and systemd snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup and status scripts for persistent scheduled watchdog execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
