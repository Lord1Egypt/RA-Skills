## Description: <br>
Generates presentations by extracting visual style from a reference PPT or PDF template and recreating slides from scratch using PptxGenJS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wujiaming88](https://clawhub.ai/user/wujiaming88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and presentation creators use this skill to turn a reference deck or PDF style into new PPTX presentations with matching layouts, typography, colors, and placeholders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded or local presentation templates may contain confidential content and can be saved in the workspace for reuse. <br>
Mitigation: Use non-confidential templates when possible, and delete retained templates plus extracted style files after the deck is generated. <br>
Risk: The workflow runs local document-conversion and extraction scripts over user-provided presentation files. <br>
Mitigation: Process trusted files in a controlled workspace and review the generated presentation before sharing or publishing it. <br>


## Reference(s): <br>
- [PPT from Template on ClawHub](https://clawhub.ai/wujiaming88/ppt-from-template) <br>
- [Style Schema](references/style-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with YAML style data, PptxGenJS JavaScript, shell commands, and generated PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses reference templates up to 50 MB, targets generated PPTX output under 20 MB, and may use image or video placeholders to control file size.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
