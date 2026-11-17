## Description:

Build multi-project Kanban systems with deterministic board discovery, consistent task processing, and persistent routing memory across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent maintain project-specific Kanban boards, route each workspace to the right board, and apply consistent task movement, WIP, and logging rules across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist local board state, routing metadata, workspace paths, aliases, and logs.

Mitigation: Use explicit-only or selected-project activation unless persistent Kanban behavior is desired for planning conversations.

Risk: Board updates can affect files under ~/kanban/ or a project .kanban directory.

Mitigation: Confirm the intended project scope before writes and review board, rules, registry, and log changes when adopting the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/kanban)
- [Skill Homepage](https://clawic.com/skills/kanban)
- [Setup](artifact/setup.md)
- [Discovery Protocol](artifact/discovery-protocol.md)
- [Board Template](artifact/board-template.md)
- [Processing Rules](artifact/processing-rules.md)
- [Memory Template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance, Files]

**Output Format:** [Markdown files and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Kanban board, rules, registry, memory, and log files under ~/kanban/ or a project .kanban directory.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
