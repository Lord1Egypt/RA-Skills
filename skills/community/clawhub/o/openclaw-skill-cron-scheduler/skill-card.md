## Description: <br>
Manage cron jobs on macOS/Linux - list, add, remove, backup, and schedule recurring tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppopen](https://clawhub.ai/user/ppopen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to inspect, add, remove, back up, restore, and manage scheduled cron tasks on macOS or Linux systems. Review proposed schedule changes carefully because the server security summary notes that this skill can create persistent scheduled commands, delete cron entries, and run sudo service-control actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ppopen/openclaw-skill-cron-scheduler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose crontab edits, backup or restore actions, and cron service commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
