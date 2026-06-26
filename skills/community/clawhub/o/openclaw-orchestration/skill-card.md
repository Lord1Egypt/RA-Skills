## Description: <br>
Framework for coordinating multi-agent tasks with atomic claims, dependencies, retries, and Markdown task visibility using a shared SQLite queue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frank-bot07](https://clawhub.ai/user/frank-bot07) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multi-agent work through a local task queue with agent registration, task claiming, dependency tracking, retries, backups, and Markdown status output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared local task state can be read or changed by agents and related workspace code that can access the SQLite database or generated Markdown files. <br>
Mitigation: Install and run the skill only in workspaces where participating agents and sibling interchange code are trusted. <br>
Risk: Task descriptions, result summaries, and failure reasons may be stored in SQLite and regenerated into Markdown status files. <br>
Mitigation: Do not place secrets, credentials, or sensitive data in task text, result summaries, or failure reasons. <br>
Risk: Restore replaces the local orchestration database. <br>
Mitigation: Keep separate backups before restore operations and close active database users before replacing the database. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/frank-bot07/openclaw-orchestration) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Package metadata](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and generated Markdown interchange files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local SQLite database as the source of truth and can generate Markdown projections for queue, agent, schema, and task state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
