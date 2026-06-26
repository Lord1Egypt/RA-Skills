## Description: <br>
墨记 is a daily task tracking skill that helps an agent create, update, follow up on, summarize, and roll over local Markdown task files through scheduled prompts and chat interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afeicn](https://clawhub.ai/user/afeicn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Managers, founders, consultants, and other daily planning users use this skill to maintain a local Markdown record of tasks, progress, and end-of-day carryover. Agents use it during scheduled morning, noon, and evening prompts or user-initiated chat updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled cron prompts may create recurring reminders or write updates at 09:00, 12:00, and 18:00. <br>
Mitigation: Review the generated cron JSON, schedule, channel, and prompts before enabling the skill. <br>
Risk: Task notes are stored in local Markdown files and may contain sensitive work details if users include them. <br>
Mitigation: Avoid recording secrets or highly sensitive information in task notes, and review the tasks directory before sharing or migrating it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/afeicn/moji-daily) <br>
- [Workflow reference](references/workflow.md) <br>
- [Daily task template](assets/daily-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown task files, cron JSON configuration, and chat guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores daily task history in local tasks/YYYY-MM-DD.md files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
