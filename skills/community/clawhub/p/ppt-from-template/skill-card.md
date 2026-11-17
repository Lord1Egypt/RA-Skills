## Description:

Generate presentations by extracting visual style from a reference template and recreating slides from scratch using PptxGenJS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujiaming88](https://clawhub.ai/user/wujiaming88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to create new PPTX decks that match a supplied PPTX or PDF template's visual style, including template discovery, style extraction, placeholder handling, and large-deck generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans the workspace template folder and may reuse saved PPTX templates.

Mitigation: Use templates from trusted sources and confirm the selected template when a generic PPT request could match template-based generation.

Risk: The skill runs local document-conversion tools on presentation files.

Mitigation: Process only trusted PPTX/PDF inputs and keep conversion dependencies available and maintained.

## Reference(s):

- [Style Schema](artifact/references/style-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/wujiaming88/skills/ppt-from-template)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, YAML style configuration, JavaScript/PptxGenJS code, and generated PPTX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Template files are limited to 50 MB and generated PPTX output targets less than 20 MB.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
