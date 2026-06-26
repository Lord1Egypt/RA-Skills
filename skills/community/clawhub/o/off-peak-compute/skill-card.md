## Description: <br>
Schedules queued, non-time-sensitive compute tasks to run overnight via cron so agents can handle batch work during off-peak capacity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willificent](https://clawhub.ai/user/willificent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up a cron-based queue for batch research, document summarization, model-intensive analysis, and other non-urgent jobs that can run unattended at 2 AM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended scheduled tasks run with the user's privileges and available credentials. <br>
Mitigation: Inspect and manually test every task before scheduling it, avoid embedding secrets, and prefer a low-privilege environment with scoped credentials. <br>
Risk: The packaged script includes active example tasks that can post online, read local context, write files, and rerun nightly. <br>
Mitigation: Remove the preloaded tasks before installing, start with an empty task list, and remove completed tasks after each run. <br>
Risk: A recurring cron entry can repeat work unexpectedly if queued tasks are left in place. <br>
Mitigation: Use one-shot scheduling for sensitive work or review the queue and logs after each overnight run. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/willificent/off-peak-compute) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with bash script and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a cron schedule and an editable shell task queue.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
