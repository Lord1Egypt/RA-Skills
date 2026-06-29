## Description: <br>
Repair and maintain PowerPoint PPTX templates with slide masters, placeholders, theme fonts, theme colors, chart links, and branded layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Brand teams, consultants, presentation operations teams, and developers use this skill to diagnose and repair PowerPoint template failures involving slide masters, layouts, placeholders, themes, charts, media relationships, and branded deck generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate automatically for general PowerPoint repair requests. <br>
Mitigation: Invoke the skill explicitly when tighter control is needed, or review the manifest wording before deployment. <br>
Risk: Template repair can damage brand fidelity or break linked PowerPoint parts if edits are made at the wrong layer. <br>
Mitigation: Preserve the original PPTX, work from a copy, map issues to the correct master, layout, slide, theme, chart, media, or relationship layer, and validate structurally and visually. <br>


## Reference(s): <br>
- [Requirement Plan](references/requirement-plan.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/powerpoint-pptx-layout-export-helper-2-180322) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with diagnoses, repair plans, code or OOXML snippets, and validation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PowerPoint part paths, placeholder mappings, relationship checks, and visual or structural validation results.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
