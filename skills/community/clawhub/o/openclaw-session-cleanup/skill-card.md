## Description:

Diagnose and stabilize long-running OpenClaw deployments that accumulate stale sessions, unreaped agents, browser-control timeouts, gateway websocket 1006 closures, or memory pressure on small VPS hosts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neoch3n](https://clawhub.ai/user/neoch3n)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to diagnose stale OpenClaw sessions, gateway instability, browser-control timeouts, and memory pressure on small long-running hosts. It guides cleanup, runtime limit tuning, recurring prune jobs, watchdog setup, and related operational safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer guidance may rely on remote shell execution that is not pinned to a reviewed release.

Mitigation: Prefer ClawHub installation or a pinned, reviewed release, and inspect installer content before running it.

Risk: Automation can create persistent cron or watchdog behavior on the host.

Mitigation: Enable recurring prune jobs and watchdog timers only after reviewing the commands and accepting the persistent host changes.

Risk: Watchdog setup may require privileged system service changes.

Mitigation: Do not run installers as root unless required, and review systemd unit installation paths and permissions before enabling services.

Risk: Session clear, gateway restart, swap setup, or watchdog actions may interrupt active OpenClaw work.

Mitigation: Use prune and runtime-limit changes first, schedule disruptive actions deliberately, and confirm recovery with OpenClaw status checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neoch3n/skills/openclaw-session-cleanup)
- [Project homepage](https://github.com/NeoCh3n/openclaw-session-cleanup-skill)
- [OpenClaw Skills documentation](https://docs.openclaw.ai/tools/skills)
- [OpenClaw Creating Skills documentation](https://docs.openclaw.ai/tools/creating-skills)
- [OpenClaw ClawHub documentation](https://docs.openclaw.ai/tools/clawhub)
- [OpenClaw session cleanup runbook](docs/openclaw.session_cleanup_v1.md)
- [OpenClaw runtime template](templates/openclaw.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose cron, systemd, swap, and OpenClaw session cleanup actions; review before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
