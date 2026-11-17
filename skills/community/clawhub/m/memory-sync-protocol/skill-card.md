## Description:

Synchronize durable behavior or preference changes across TOOLS.md, MEMORY.md, AGENTS.md, and memory/YYYY-MM-DD.md with one consistent workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markisadesigner1992-eng](https://clawhub.ai/user/markisadesigner1992-eng)

### License/Terms of Use:


## Use Case:

Developers and maintainers use this skill to keep durable agent memory, routing rules, governance notes, and daily change logs synchronized when users ask an agent to remember or update operating conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change agent memory, routing, governance files, daily logs, and git history.

Mitigation: Require the agent to show the proposed diff, confirm target files, and ask separately before creating commits.

Risk: The skill could store secrets or credentials in durable memory files if safeguards are not enforced.

Mitigation: Refuse to store secrets or credentials and review changes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/markisadesigner1992-eng/skills/memory-sync-protocol)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown sync report with proposed or applied file updates and commit details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update durable memory, routing, governance, daily log files, and git history when installed and executed by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
