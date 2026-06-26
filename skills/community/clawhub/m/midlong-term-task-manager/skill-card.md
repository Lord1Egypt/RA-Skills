## Description: <br>
Manages and tracks an AI agent's mid- and long-term tasks, including task decomposition, progress updates, deadline reminders, and daily or weekly summary generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrot90-code](https://clawhub.ai/user/harrot90-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep multi-day or multi-month work organized through task registration, status tracking, heartbeat checks, and periodic Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task names, descriptions, logs, and summaries are retained locally and may contain sensitive project details. <br>
Mitigation: Avoid recording secrets or highly sensitive details in tasks; review local files under ~/.openclaw/workspace/.tasks before sharing or archiving them. <br>
Risk: Heartbeat or cron integration can generate recurring local task logs and reports. <br>
Mitigation: Enable the heartbeat and cron examples only intentionally, and confirm the configured workspace path before scheduling the scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrot90-code/midlong-term-task-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, local JSON task records, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes task records, logs, daily summaries, and weekly reports under ~/.openclaw/workspace/.tasks.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
