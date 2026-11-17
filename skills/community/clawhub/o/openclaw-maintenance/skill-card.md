## Description:

Provides local maintenance scripts for monitoring and maintaining OpenClaw Gateway health, proxy connectivity, safe restarts, and log cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jesson1222-ship-it](https://clawhub.ai/user/jesson1222-ship-it)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to deploy and operate OpenClaw maintenance scripts that monitor Gateway availability, respond to proxy or queue issues, perform safe restarts, and clean local logs across macOS, Linux, and NAS environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Linux systemd guidance can create a root-level watchdog that runs a script from a user-writable home directory.

Mitigation: Install the service under the intended least-privilege user or move scripts to a root-owned path before enabling systemd.

Risk: .env values may contain CLASH_SECRET and notification targets.

Mitigation: Restrict file permissions, avoid committing secrets, and rotate exposed credentials before deployment.

Risk: The scripts can automatically restart OpenClaw Gateway and switch proxy nodes.

Mitigation: Review thresholds, endpoints, notification settings, and cooldown behavior in a staging or maintenance window before production use.

Risk: The log cleanup script deletes old or oversized OpenClaw log files.

Mitigation: Confirm retention requirements and back up logs that may be needed for incident review before scheduling cleanup.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jesson1222-ship-it/skills/openclaw-maintenance)
- [README](artifact/README.md)
- [Proxy Health Monitor README](artifact/README-proxy-health.md)
- [Agent Quickstart](artifact/AGENT.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational scripts for local installation, health checks, proxy switching, safe restart, and log cleanup.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
