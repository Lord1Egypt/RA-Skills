## Description: <br>
Replicates slide screenshots, slide photos, and design mockups into editable PPTX files by restoring layout, colors, text, and graphic elements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dami2010](https://clawhub.ai/user/dami2010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, designers, and developers use this skill to convert screenshots, slide photos, and mockups into editable PowerPoint decks while preserving the visible structure, text, colors, and shapes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The OCR helper can install system and Python packages during normal use. <br>
Mitigation: Run the skill in a container or isolated environment, and preinstall and pin OCR dependencies before use when possible. <br>
Risk: Input screenshots, previews, and generated outputs may contain confidential visual content. <br>
Mitigation: Avoid processing confidential screenshots unless the execution environment and output storage locations are controlled. <br>


## Reference(s): <br>
- [Image To PPT Pro ClawHub Page](https://clawhub.ai/dami2010/image-to-ppt-pro) <br>
- [PptxGenJS API Quick Reference](references/pptxgenjs-cheatsheet.md) <br>
- [PPT Shape Recognition and Code Quick Reference](references/shapes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript, Python, and shell snippets, plus generated PPTX files when the workflow is executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use OCR and color extraction helpers, a coordinate preflight checker, and iterative visual QA before delivery.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
