## Description: <br>
Provides junior-high mathematics teaching resources, lesson plan generation, exercise planning, and teaching progress support based on the 2024 People's Education Press curriculum materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ymf508](https://clawhub.ai/user/ymf508) <br>

### License/Terms of Use: <br>
教育用途免费 <br>


## Use Case: <br>
Mathematics teachers and education staff use this skill to locate grade-specific resource indexes, draft lesson or semester plans, create practice material outlines, and organize review plans for grades 7 through 9. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests local command-execution permission that is broader than the visible teaching-resource and plan-generation behavior requires. <br>
Mitigation: Review the skill before installing, grant only permissions needed in the target environment, and restrict command execution where possible. <br>
Risk: Resource indexes reference local Windows teaching-material paths that may not exist or may expose local file organization assumptions. <br>
Mitigation: Confirm referenced resource locations before classroom use and replace local paths with approved institutional locations if needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ymf508/junior-high-math-research-plans) <br>
- [README](artifact/README.md) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [Seventh Grade Resource Index](artifact/resources/七年级资源索引.md) <br>
- [Eighth Grade Resource Index](artifact/resources/八年级资源索引.md) <br>
- [Ninth Grade Resource Index](artifact/resources/九年级资源索引.md) <br>
- [Lesson Plan Template](artifact/templates/教学计划模板.md) <br>
- [Study Guide Template](artifact/templates/学案模板.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown, plain text, JSON-like JavaScript objects, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include grade, chapter, keyword, schedule, and template-filled teaching-plan details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
