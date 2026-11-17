## Description:

规划并制作课程汇报、工作汇报、项目汇报、答辩等 PPT。根据主题、时长、人员分工和参考资料，先生成完整页面框架、章节分配与逐页讲稿要点，待用户确认后，再按指定主题和视觉风格生成 PPT 文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptocxf](https://clawhub.ai/user/cryptocxf)

### License/Terms of Use:

MIT-0

## Use Case:

Students, educators, and business users can use this skill to turn a presentation topic, duration, team assignments, and reference materials into a structured PPT plan with page-by-page speaker notes. After the user confirms the plan, the skill can guide generation of a PowerPoint file that follows the confirmed structure and visual style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to create PPT files, and the artifact contains conflicting instructions about whether file generation requires explicit confirmation.

Mitigation: Review the plan before execution, use an outline-only instruction until ready to create files, and confirm the output path, filename, and any pip install before allowing .pptx generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cryptocxf/skills/group-ppt-outline)
- [PPTX generation reference](references/pptx-generation.md)
- [Presentation outline templates](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance, files]

**Output Format:** [Markdown guidance with optional Python and shell command snippets, plus generated .pptx files after confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a two-stage workflow: first a confirmed presentation plan, then optional PPTX generation with speaker notes and visible placeholders for missing facts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
