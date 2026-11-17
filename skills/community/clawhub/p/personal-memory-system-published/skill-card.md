## Description:

Personal Memory System Published helps an agent sync long-term notes from a local MEMORY.md file into a searchable SQLite memory database for later retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awublack](https://clawhub.ai/user/awublack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to keep personal notes in a local Markdown file while giving an agent a structured SQLite index for memory lookup and summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal notes in MEMORY.md may be duplicated into memory.db automatically.

Mitigation: Install only in workspaces where local database copies of personal notes are acceptable, and protect both files with the same access controls.

Risk: Heartbeat sync can replace existing memory database contents.

Mitigation: Back up MEMORY.md and memory.db before enabling automatic sync or changing the memory file structure.

Risk: Natural-language questions may lead an agent to generate unsafe or overly broad SQL.

Mitigation: Use a constrained read-only query function for memory lookup and review generated SQL before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/awublack/skills/personal-memory-system-published)
- [Publisher profile](https://clawhub.ai/user/awublack)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell commands, and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file and SQLite database operations are expected; no external API output is described.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
