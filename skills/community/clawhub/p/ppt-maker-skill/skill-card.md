## Description: <br>
根据一句话主题、Markdown 或已有文稿生成结构化 PPT，并支持自然语言修改页面与组件后导出为可编辑 PPT。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mr-q526](https://clawhub.ai/user/mr-q526) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to create structured presentation projects from a topic, Markdown, or draft text, then preview, edit, validate, and export editable PPTX files. It is suited to repeatable deck workflows that keep slide content in deck.json rather than ad hoc HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes project files, previews, and PPTX exports in its workspace. <br>
Mitigation: Confirm project and export paths before running build, preview, export, or subskill creation commands. <br>
Risk: Source documents placed in materials/ may contain sensitive content used during deck creation. <br>
Mitigation: Only add needed materials, remove sensitive files after use, and review generated deck.json and PPTX outputs before sharing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mr-q526/ppt-maker-skill) <br>
- [Slide Schema](references/slide-schema.md) <br>
- [Layout Rules](references/layout-rules.md) <br>
- [Template Catalog](references/template-catalog.md) <br>
- [Prompt Patterns](references/prompt-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance, JSON deck structures, Node.js shell commands, HTML preview files, and PPTX exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates project files in its workspace and can export editable .pptx presentations from deck.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
