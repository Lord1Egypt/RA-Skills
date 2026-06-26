## Description: <br>
Converts PPT screenshots or infographics into editable PPTX files using VLM-based region understanding, coordinate mapping, and PNG fallback for complex shapes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allergro](https://clawhub.ai/user/allergro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and presentation authors use this skill to analyze slide screenshots, map detected regions into PPT coordinates, and generate editable PPTX output. It is also useful when a source PPTX is available and text replacement should preserve original slide structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slide screenshots may be sent to the configured VLM provider during image analysis. <br>
Mitigation: Use only with slides approved for that provider and avoid confidential, sensitive, or unauthorized decks. <br>
Risk: The workflow reads and writes local temporary PNG files and generated PPTX files. <br>
Mitigation: Keep input and output paths inside the project folder and review generated files before sharing or deploying them. <br>
Risk: Runtime dependencies are installed outside the skill package. <br>
Mitigation: Install pptxgenjs and Pillow from trusted sources and keep the runtime environment constrained to the intended project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allergro/ppt-vision-replica) <br>
- [Region schema](references/region_schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with JSON region structures, JavaScript and Python snippets, shell commands, and generated PPTX/PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a configured VLM provider for image analysis and may read or write local temporary PNG and PPTX files.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence; artifact frontmatter states 1.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
