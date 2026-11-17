## Description:

家庭教育习惯养成追踪与教育付出记录系统，用于在用户提及习惯养成、坏习惯干预、孩子行为变化记录、干预效果分析、教育付出总结或孩子内驱力建立时，帮助记录、查询和分析相关家庭教育信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[silent404](https://clawhub.ai/user/silent404)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and family education assistants use this skill to track child habit formation, habit interventions, education contributions, motivation-related signals, and progress statistics in a local SQLite record system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist and modify sensitive child and family education records.

Mitigation: Treat the SQLite database as private family data and use appropriate backups and access controls.

Risk: Broad activation and insufficient confirmation could lead to unintended create, update, archive, merge, or delete actions.

Mitigation: Require explicit user confirmation before every record-changing action.

## Reference(s):

- [Database Schema Reference](references/schema.md)
- [ClawHub Skill Page](https://clawhub.ai/silent404/skills/habit-education)
- [Publisher Profile](https://clawhub.ai/user/silent404)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Chinese-language conversational guidance with Python script calls and structured record summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists and updates local SQLite records for child habits, interventions, archived summaries, and education contributions.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
