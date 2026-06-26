## Description: <br>
Helps agents configure OpenClaw Gateway cron jobs for one-time reminders, recurring tasks, background automation, delivery channels, and webhook delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zyclincoln](https://clawhub.ai/user/zyclincoln) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create, inspect, run, edit, and remove scheduled OpenClaw jobs. It is useful for configuring main-session reminders, isolated background tasks, cron schedules, delivery behavior, retention, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled task results may be sent to chat channels or webhooks, which can expose private, personal, health, or business-sensitive information. <br>
Mitigation: Review each job's prompt, schedule, retention, and delivery mode before enabling it; use delivery mode none for private tasks and avoid sending sensitive data to external channels. <br>
Risk: Persistent scheduled tasks can run repeatedly or in the background after configuration. <br>
Mitigation: List and review enabled cron jobs regularly, remove unneeded jobs, and confirm that Gateway scheduling, time zone, and retention settings match the intended automation. <br>


## Reference(s): <br>
- [OpenClaw Cron Jobs Documentation](https://docs.openclaw.ai/automation/cron-jobs) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw cron command examples, schedule schema examples, delivery modes, storage paths, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
