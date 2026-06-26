## Description: <br>
Novel Director helps users direct interactive long-form fiction by setting scenes, characters, goals, and choices while the agent writes staged story segments and manages continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caoyachao](https://clawhub.ai/user/caoyachao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and creative teams use this skill to co-create serial fiction through a director-style loop: they define scenes and decisions while the agent drafts short story segments, tracks world and chapter context, and resumes projects across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Story projects may retain sensitive or personal information in local draft, chapter, index, and world-knowledge files. <br>
Mitigation: Use explicit project names, avoid storing sensitive personal information in story projects, and review or delete local project folders when retention is no longer desired. <br>
Risk: Saved continuity data can influence later story output and may carry forward outdated or unwanted character, timeline, or plot details. <br>
Mitigation: Review saved chapter indexes and world or character notes before resuming a project, and edit or remove stale context before continuing. <br>


## Reference(s): <br>
- [Skill definition](SKILL.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Interactive Markdown prose with local JSON project context files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save drafts, chapters, chapter indexes, and world or character notes in local project files for continuity.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
