## Description: <br>
OpenClaw Guardian deploys and manages a watchdog for OpenClaw Gateway that monitors health, runs doctor --fix, rolls back a git-backed workspace, takes daily snapshots, and can send Discord alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeoYeAI](https://clawhub.ai/user/LeoYeAI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to install and manage an unattended OpenClaw Gateway watchdog with self-repair, git rollback, daily snapshots, and optional Discord status notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The watchdog can keep running and automatically modify, commit, hard-reset, and restart an OpenClaw workspace without per-action approval. <br>
Mitigation: Install it only for workspaces where unattended recovery is intended; use a dedicated git-backed workspace, set GUARDIAN_WORKSPACE explicitly, and keep backups or stash important changes. <br>
Risk: Rollback and repair behavior may replace local workspace state when the gateway is detected as unhealthy. <br>
Mitigation: Test the recovery flow before production use and confirm the selected stable commit and backup process are acceptable for the workspace. <br>
Risk: Discord webhook alerts can send external status notifications if DISCORD_WEBHOOK_URL is configured. <br>
Mitigation: Leave DISCORD_WEBHOOK_URL unset unless external notifications are approved for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LeoYeAI/myclaw-guardian) <br>
- [MyClaw.ai homepage](https://myclaw.ai) <br>
- [OpenClaw Guardian documentation](https://github.com/LeoYeAI/openclaw-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference required binaries git, pgrep, and curl, and optional DISCORD_WEBHOOK_URL notifications.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
