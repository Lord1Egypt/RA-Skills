## Description: <br>
Guzhou Novel Studio is a Chinese-language novel-writing workflow skill that routes user requests across research, drafting, style management, quality review, and long-form project management modules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guzhoutingyu](https://clawhub.ai/user/guzhoutingyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External writers and creative teams use this skill to plan, draft, revise, style-check, and quality-review Chinese fiction projects from short stories through long-form serialized novels. It is designed to coordinate outlines, character data, timeline notes, chapter prose, style references, memory files, and QA reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently rewrite project files and includes a self-evolution workflow that updates skill instructions and writing-style references. <br>
Mitigation: Use it only in an intended project workspace, keep backups, require visible diffs, and obtain explicit approval before overwriting skill instructions, style files, outlines, memory files, or reports. <br>
Risk: The skill may read and persist unpublished manuscript content, character data, timelines, and style samples. <br>
Mitigation: Keep sensitive or unpublished manuscripts outside the workspace unless the user intends the skill to process and store them. <br>
Risk: Creative plans, QA findings, and generated prose may contain continuity mistakes, misleading recommendations, or unwanted style imitation. <br>
Mitigation: Review generated outlines, chapters, style documents, and QA reports before publication or downstream reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guzhoutingyu/guzhou-novel-studio) <br>
- [Workflow guide](references/workflow-guide.md) <br>
- [File format specification](references/file-format-spec.md) <br>
- [Researcher checklists](modules/researcher/references/checklists.md) <br>
- [Researcher output templates](modules/researcher/references/output-templates.md) <br>
- [QA check dimensions](modules/qa/references/check-dimensions.md) <br>
- [Studio writing style reference](modules/studio/references/writing-style.md) <br>
- [Style dimensions](modules/stylist/references/style-dimensions.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance, Configuration] <br>
**Output Format:** [Chinese-language prose, Markdown reports and chapters, structured JSON project files, and project configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project outlines, chapter drafts, memory files, style files, and QA reports in the active workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and root SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
