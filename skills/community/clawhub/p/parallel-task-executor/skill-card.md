## Description: <br>
Coordinates multiple user instructions as parallel or serial tasks with priority scheduling, dependency handling, progress tracking, retries, and execution reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Erichy777](https://clawhub.ai/user/Erichy777) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to break a multi-part request into tracked tasks, schedule them by priority and dependency, and summarize completion or failure across concurrent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages broad concurrent file, shell, network, API, and database actions. <br>
Mitigation: Require the agent to show the planned task list before execution and obtain explicit approval for deletes, writes, uploads, shell or script execution, API mutations, database actions, retries, and background work. <br>
Risk: Parallel retries and background work can amplify mistakes or resource usage. <br>
Mitigation: Use narrow directory, command, account, domain, concurrency, timeout, and retry limits before enabling task execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Erichy777/parallel-task-executor) <br>
- [Task priority specification](references/priorities.md) <br>
- [Execution report format](references/reports.md) <br>
- [Scheduling algorithm notes](references/scheduler.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured task or report snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task queues, priority labels, progress summaries, retry status, and execution reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
