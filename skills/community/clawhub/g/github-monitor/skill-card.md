## Description: <br>
Monitor one or more GitHub repositories and send low-noise alerts with configurable policy modes (major_only, balanced, verbose). Use when setting up recurring repo watch, release/security monitoring, PR merge tracking, and daily digest workflows via OpenClaw cron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samwei12](https://clawhub.ai/user/samwei12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure recurring monitoring for one or more GitHub repositories, covering releases, recent commits, merged pull requests, security signals, breaking-change signals, and daily digests through OpenClaw cron. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A recurring monitor can continue checking repositories and sending alerts until its scheduled job is changed or removed. <br>
Mitigation: Before installing, confirm the repository list, cron interval, notification destination, and state-file path, and update or remove the scheduled job when monitoring is no longer needed. <br>
Risk: Incorrect cursor or state-file setup can create noisy alerts, duplicate notifications, or historical backfill. <br>
Mitigation: Initialize installed_at, last_checked_at, and last_notified_at to the first-run time, persist state after successful scans, and keep the state file stable across restarts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samwei12/github-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration guidance] <br>
**Output Format:** [Markdown brief impact summaries with on-demand event details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configurable policy modes, stateful deduplication, daily digest queues, and concise impact-first notifications.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
