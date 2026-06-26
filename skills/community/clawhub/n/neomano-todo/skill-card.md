## Description: <br>
Enhanced TODO/task manager backed by a local SQLite database with priorities, tags, due dates, reminder timestamps, explicit task lifecycle statuses, and stale-task detection to prevent backlog accumulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elandivar](https://clawhub.ai/user/elandivar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and agents use this skill to create, list, filter, prioritize, update, complete, expire, forget, and review personal tasks in a local SQLite-backed task store. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task titles, notes, due dates, and reminder metadata may contain sensitive personal or work information stored in the local SQLite database. <br>
Mitigation: Configure the database path deliberately, limit local file access, and avoid storing secrets or unnecessary sensitive details in task fields. <br>
Risk: Reminder metadata can route notifications to an unintended channel, target, or timezone if configured incorrectly. <br>
Mitigation: Verify reminder channel, target, and timezone settings before enabling scheduled reminders or storing cron job identifiers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elandivar/neomano-todo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-producing helper commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper script commands return JSON for agent parsing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
