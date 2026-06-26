## Description: <br>
Pptx Master is an AI-assisted presentation workflow that converts PDF, DOCX, URL, Markdown, and other source material into editable SVG-based PowerPoint presentations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, consultants, and presentation authors use this skill to turn source documents, web pages, and structured content into professional editable PPTX decks with templates, SVG generation, image tooling, quality checks, and export steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local scripts and write project files. <br>
Mitigation: Install and run it only in a workspace where local script execution and generated presentation files are acceptable. <br>
Risk: The skill includes broad URL fetching for web-to-Markdown conversion. <br>
Mitigation: Process only trusted URLs and review fetched content before using it in generated presentations. <br>
Risk: The skill can use credentialed image-provider backends through environment variables. <br>
Mitigation: Keep .env files limited to the selected provider and avoid storing unrelated credentials in the skill workspace. <br>
Risk: The bundle includes a watermark-removal utility. <br>
Mitigation: Avoid using the watermark-removal tool unless the user has rights to modify the image. <br>
Risk: The bundle includes a repository update script. <br>
Mitigation: Review any planned use of update_repo.py before executing it. <br>
Risk: The workflow processes SVG and rotation task JSON files. <br>
Mitigation: Use trusted SVG and task JSON inputs and review generated files before export. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vincentlau2046-sudo/pptx-master) <br>
- [README](README.md) <br>
- [Script documentation index](scripts/README.md) <br>
- [Canvas formats](references/canvas-formats.md) <br>
- [Strategist workflow reference](references/strategist.md) <br>
- [Image generation reference](references/image-generator.md) <br>
- [Shared standards](references/shared-standards.md) <br>
- [Template documentation](templates/README.md) <br>
- [SVG specification](http://www.w3.org/2000/svg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, project configuration, SVG content, and PPTX export artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write project files, convert source material, generate or post-process images and SVG, validate presentation quality, and export PPTX files.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata and CHANGELOG, released 2026-05-07) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
