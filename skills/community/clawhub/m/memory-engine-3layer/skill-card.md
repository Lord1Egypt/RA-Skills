## Description: <br>
Memory Engine gives OpenClaw agents persistent, capacity-managed local memory with daily logs, long-term and user profile stores, search, session extraction, cron and watcher maintenance, snapshots, and backup or restore workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zacko2o](https://clawhub.ai/user/zacko2o) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external OpenClaw users use Memory Engine to persist, search, and maintain agent memory across sessions. It supports daily logs, long-term memory, user preferences, session recovery, health checks, capacity checks, and local search indexing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local capture can store sensitive session content, durable memory, and user profile data. <br>
Mitigation: Enable the skill only when persistent memory is intended, review generated memory files, avoid storing secrets, and keep workspace file permissions appropriate. <br>
Risk: GitHub backup can move private memory and configuration data to a remote repository, and token-bearing remote URLs can expose credentials. <br>
Mitigation: Use only a private, intentionally selected repository, avoid embedding tokens in remote URLs, and inspect what git will commit before backup. <br>
Risk: Cron and watcher processes can continue running in the background and perform memory extraction, indexing, snapshots, and backup attempts. <br>
Mitigation: Review installed crontab entries, watcher process state, and logs; disable the cron or watcher if background maintenance is not desired. <br>
Risk: Restore can reintroduce configuration, installed skills, rule files, personality files, and scheduled tasks from a backup. <br>
Mitigation: Treat restore as an administrative action and review restored openclaw.json, skills, rule or personality files, and crontab before applying them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zacko2o/memory-engine-3layer) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Changelog](artifact/CHANGELOG.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>
- [OpenClaw Project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown and JSON summaries, local Markdown memory files, SQLite search artifacts, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads local OpenClaw workspace memory files; search results are truncated snippets with file citations; backup and restore may use git when configured.] <br>

## Skill Version(s): <br>
6.0.0 (source: evidence release metadata and CHANGELOG, released 2026-04-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
