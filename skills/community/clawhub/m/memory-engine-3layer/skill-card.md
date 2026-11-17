## Description:

Memory Engine helps OpenClaw agents preserve, search, maintain, back up, and restore persistent memory across sessions with capacity controls, snapshots, and background health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zacko2o](https://clawhub.ai/user/zacko2o)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using OpenClaw use this skill to create, retrieve, maintain, compact, back up, and restore durable agent memory while controlling memory growth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and active session monitoring can retain sensitive conversation data.

Mitigation: Install only in workspaces where persistent memory is expected; keep memory files and backups private, and remove cron or watcher setup when background monitoring is not desired.

Risk: Backup and restore operations can expose or overwrite OpenClaw workspace data.

Mitigation: Avoid token-in-URL Git remotes, use narrowly scoped private repositories, and restore only from repositories you have personally verified.

Risk: Hourly cron and watcher processes run outside active agent turns.

Mitigation: Review cron entries before enabling, monitor memory logs, and disable cron if continuous background execution is not acceptable.

## Reference(s):

- [Memory Engine on ClawHub](https://clawhub.ai/zacko2o/skills/memory-engine-3layer)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Full documentation](SKILL.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with shell commands, JSON status output, configuration snippets, and local memory files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and maintains local OpenClaw memory files, SQLite search indexes, snapshots, cron logs, and optional Git backups.]

## Skill Version(s):

6.0.0 (source: server release metadata and changelog, released 2026-04-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
