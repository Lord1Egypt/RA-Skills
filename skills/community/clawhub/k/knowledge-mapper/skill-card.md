## Description:

Notes Knowledge Mapper analyzes Markdown and text notes to extract entities, relationships, searchable summaries, and graph views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and note-taking users use this skill to turn local Markdown or text collections into searchable knowledge maps with entity lists, relationship summaries, and exportable graph formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The inspected artifact does not include the knowledge-graph CLI implementation.

Mitigation: Confirm the executable implementation is present and review it before installing or running the skill.

Risk: Imported notes are stored persistently in a local SQLite database.

Mitigation: Avoid importing sensitive documents unless users have a retention and deletion plan for ~/.openclaw/data/knowledge-graph/.

Risk: Graph image generation depends on optional GraphViz tooling.

Mitigation: Install GraphViz before using DOT-to-image workflows, or rely on text and JSON exports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/knowledge-mapper)
- [English skill documentation](artifact/SKILL_EN.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, GraphViz DOT, shell commands, guidance]

**Output Format:** [Markdown guidance with CLI commands and exported text, JSON, or GraphViz DOT artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist imported note data in a local SQLite database under ~/.openclaw/data/knowledge-graph/.]

## Skill Version(s):

1.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
