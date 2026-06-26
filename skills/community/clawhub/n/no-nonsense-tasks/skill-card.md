## Description: <br>
A SQLite-backed task manager for tracking tasks with statuses, descriptions, and tags through add, list, filter, update, move, and delete commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dvjn](https://clawhub.ai/user/dvjn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI agents use this skill to maintain a local SQLite task list for personal tasks, project tracking, and status-based workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task data is stored in a local SQLite database that may contain sensitive task text if users put secrets into tasks. <br>
Mitigation: Configure the database path deliberately and avoid storing secrets or credentials in task titles, descriptions, or tags. <br>
Risk: Update and delete commands can modify or remove task records. <br>
Mitigation: Review task IDs and command intent before running update or delete operations when the task list matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dvjn/no-nonsense-tasks) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [AGENT.md](AGENT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text and markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and reads a local SQLite task database at ~/.no-nonsense/tasks.db unless NO_NONSENSE_TASKS_DB is configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
