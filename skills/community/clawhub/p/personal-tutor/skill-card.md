## Description:

Personal Tutor helps an agent run structured learning sessions, quizzes, and post-lesson archiving into learning records, memory, and Markdown knowledge bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ben61405](https://clawhub.ai/user/ben61405)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and agent users use this skill to turn chat-based study into a repeatable workflow: subject setup, daily instruction, comprehension checks, and durable lesson archives. It is most useful when the user wants syllabi, learning logs, and optional Markdown or Obsidian-style concept notes kept in sync over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask the agent to modify persistent agent rule files after an archive failure.

Mitigation: Do not permit edits to global agent rule files such as SOUL.md, TOOLS.md, or broad memory policy files unless a human explicitly reviews and approves the exact change.

Risk: A user-provided schemaPath can be treated as higher priority than built-in knowledge-base rules.

Mitigation: Use only trusted schema files, avoid shared or synced schema locations unless fully trusted, and preview the schema path before reading it.

Risk: Archiving workflows can write to learning and knowledge-base directories.

Mitigation: Ask for a path preview and confirmation before archival writes, especially when using broad, shared, or synced directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ben61405/skills/personal-tutor)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown responses, JSON configuration examples, filesystem paths, lesson records, syllabi, and knowledge-base note content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learning logs, syllabi, memory entries, concept notes, indexes, and config files according to the user's selected archive settings.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
