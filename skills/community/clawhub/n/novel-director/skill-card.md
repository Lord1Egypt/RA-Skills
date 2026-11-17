## Description:

Novel Director helps an assistant co-write interactive serialized fiction through scene-by-scene direction, decision points, and long-form context management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoyachao](https://clawhub.ai/user/caoyachao)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and creative teams use this skill to direct AI-assisted fiction scenes, make branch decisions, and maintain long-running novel context through chapter indexes and world knowledge files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and update local novel project files during save, export, load, and chapter completion workflows.

Mitigation: Use explicit project names, avoid names containing slashes or path-like text, and review save or export actions before allowing writes.

Risk: Broad writing triggers may activate the skill during general fiction-writing requests.

Mitigation: Confirm the intended novel project and operation before loading, saving, exporting, or updating files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/caoyachao/skills/novel-director)
- [Skill Instructions](artifact/SKILL.md)
- [README](artifact/README.md)
- [World Knowledge Template](artifact/templates/world_knowledge.json)
- [Chapter Index Template](artifact/templates/chapter_index.json)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Chinese-language prose, Markdown chapter text, and JSON project state updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local novel project files when the user requests save, export, load, or chapter completion actions.]

## Skill Version(s):

2.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
