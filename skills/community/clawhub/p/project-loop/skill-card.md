## Description: <br>
Run approved long-running project work from file-backed state, continue through self-clearable tasks, pause cleanly at real gates, and recover across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebclawops](https://clawhub.ai/user/sebclawops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage approved long-running project work with file-backed state, validation, pause and approval gates, and recovery across interrupted sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to continue long-running work automatically through file-backed state and watchdog recovery. <br>
Mitigation: Use it only for approved projects with a clear owner, defined scope, explicit approval gates, and reviewed project state files. <br>
Risk: Watchdog cron behavior can create persistence that may surprise users if left enabled after project completion. <br>
Mitigation: Inspect created watchdog cron entries, confirm how to disable them, and remove watchdogs when projects reach Done or Abandoned. <br>
Risk: Retrying denied or oversized commands without review can repeat unsafe execution attempts. <br>
Mitigation: Review any denied command before retrying, split work into smaller independent steps, and stop at real blockers or failed state updates. <br>


## Reference(s): <br>
- [Project Loop on ClawHub](https://clawhub.ai/sebclawops/project-loop) <br>
- [sebclawops publisher profile](https://clawhub.ai/user/sebclawops) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with file-backed project state conventions and command recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operating instructions for project files, state transitions, validation records, approval gates, pause/resume behavior, and watchdog handling.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
