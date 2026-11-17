## Description:

Deploys and manages a Guardian watchdog for OpenClaw Gateway with health checks, self-repair, git rollback, daily snapshots, and optional Discord alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leoyeai](https://clawhub.ai/user/leoyeai)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to install and run a watchdog that keeps an OpenClaw Gateway process available and attempts automated repair or rollback when health checks fail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watchdog can automatically change, commit, reset, and restart an OpenClaw workspace.

Mitigation: Install only where persistent automated repair is desired, and gate or disable hard-reset rollback until the rollback target and consent boundary are clear.

Risk: Daily snapshots use broad git staging and may include sensitive workspace content.

Mitigation: Review workspace contents and ignore rules before use, and avoid broad staging over directories that may contain secrets or private data.

Risk: Operational details may be sent to a Discord webhook when alerts are configured.

Mitigation: Configure `DISCORD_WEBHOOK_URL` only for approved channels and avoid exposing sensitive incident or workspace details through notifications.

Risk: Logs and state default to shared `/tmp` paths.

Mitigation: Move logs and state files to workspace-owned paths with appropriate permissions before long-running deployment.

## Reference(s):

- [MyClaw.ai](https://myclaw.ai)
- [OpenClaw Guardian release page](https://clawhub.ai/leoyeai/skills/myclaw-guardian)
- [OpenClaw Guardian full docs](https://github.com/LeoYeAI/openclaw-guardian)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw plus git, pgrep, pkill, and curl when Discord alerts are enabled.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
