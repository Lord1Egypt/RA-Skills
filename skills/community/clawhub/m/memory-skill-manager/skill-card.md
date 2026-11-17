## Description:

Responsible for maintaining SKILLMEMORY.md in the target skill directory, recording the three most recent execution pipeline JSONs, and modifying the description file of the target SKILL.md to achieve progressive experience awakening upon each skill invocation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdsds222](https://clawhub.ai/user/sdsds222)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to persist sanitized execution summaries for agent skills and update target skill documentation with a memory reminder for future runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists task history that may include sensitive prompt or execution details.

Mitigation: Use only with tasks that do not involve secrets or private prompts, and review SKILLMEMORY.md after each update.

Risk: The skill edits other skill directories and appends a memory reminder to target SKILL.md files.

Mitigation: Run it only in a tightly scoped skills directory and keep backups so modified skills can be restored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdsds222/skills/memory-skill-manager)
- [Publisher profile](https://clawhub.ai/user/sdsds222)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell command invocation and generated JSON memory content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and maintains a bounded SKILLMEMORY.md history of up to three execution entries.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
