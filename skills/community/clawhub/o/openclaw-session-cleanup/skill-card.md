## Description: <br>
Diagnoses and stabilizes long-running OpenClaw deployments affected by stale sessions, unreaped agents, browser-control timeouts, gateway websocket 1006 closures, and memory pressure on small VPS hosts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NeoCh3n](https://clawhub.ai/user/NeoCh3n) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to diagnose high OpenClaw session and agent counts, recover from gateway or browser-control instability, and apply conservative runtime limits on small hosts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes real host-changing cleanup and automation commands. <br>
Mitigation: Run commands deliberately after reviewing the affected OpenClaw instance and host configuration. <br>
Risk: Remote shell installation can hide script behavior at execution time. <br>
Mitigation: Prefer cloning or downloading the artifact and inspecting scripts before running them instead of piping remote content directly to bash. <br>
Risk: `openclaw sessions clear` can terminate active production work. <br>
Mitigation: Use session pruning first and clear sessions only after confirming that active sessions can be safely ended. <br>
Risk: Cron cleanup, watchdog restarts, and swap changes can affect long-running services and disk usage. <br>
Mitigation: Enable those changes only when persistent background cleanup, possible gateway restarts, and additional disk allocation are acceptable. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/NeoCh3n/openclaw-session-cleanup) <br>
- [Publisher Profile](https://clawhub.ai/user/NeoCh3n) <br>
- [Project Homepage](https://github.com/NeoCh3n/openclaw-session-cleanup-skill) <br>
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills) <br>
- [OpenClaw Creating Skills Documentation](https://docs.openclaw.ai/tools/creating-skills) <br>
- [OpenClaw ClawHub Documentation](https://docs.openclaw.ai/tools/clawhub) <br>
- [Detailed Runbook](docs/openclaw.session_cleanup_v1.md) <br>
- [Runtime Template](templates/openclaw.json) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, cron, systemd, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
