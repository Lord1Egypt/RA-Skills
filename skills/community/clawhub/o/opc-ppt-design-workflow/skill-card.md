## Description: <br>
交互式PPT设计全流程管控，基于create-ppt技能，增加需求确认、风格预览、正式生成三阶段交互。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golngod](https://clawhub.ai/user/golngod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and presentation creators use this skill to gather PPT requirements, compare style previews, and guide create-ppt through full deck generation with QA checks for page structure, data accuracy, and text rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: One optional Vaporwave visual style may add Japanese decorative text, which can be unsuitable for presentations that must stay in one language or satisfy strict localization requirements. <br>
Mitigation: Review or edit the Vaporwave style template before using that style in localized or compliance-sensitive presentations. <br>
Risk: AI-generated slide imagery can render Chinese text, numbers, or embedded labels incorrectly. <br>
Mitigation: Use the skill's HTML text-layer workflow and post-generation QA checklist to render important text outside the image layer and verify structure, data, and encoding before delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/golngod/opc-ppt-design-workflow) <br>
- [QA checklist](references/qa_checklist.md) <br>
- [8 style prompt templates](references/style_templates.md) <br>
- [8 PPT style templates V2.0](references/style_templates_v2.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with prompt templates, HTML/CSS patterns, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only workflow guidance that may direct a separate create-ppt skill to generate PPTX-style HTML files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
