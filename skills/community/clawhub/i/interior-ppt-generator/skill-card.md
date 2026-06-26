## Description: <br>
Creates a client-facing interior design PowerPoint deck from a folder of local render images, using preset slide layouts, Chinese text, and brand styling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[137984917-cyber](https://clawhub.ai/user/137984917-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Interior designers use this skill to turn a local folder of renderings into a styled 16:9 client presentation with cover, task review, design concept, image showcase, materials, and closing slides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated decks include preset Chinese text, room names, material descriptions, and publisher branding. <br>
Mitigation: Review and edit the generated slides before client delivery, especially branding, room labels, and project-specific material descriptions. <br>
Risk: The generator builds slides from a local image folder and silently skips files that Pillow cannot verify as images. <br>
Mitigation: Use a reviewed local image folder, confirm filenames are ordered as intended, and check the final slide count and image coverage after generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/137984917-cyber/interior-ppt-generator) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Skill manifest](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands; generated output is a .pptx file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local png, jpg, jpeg, webp, and bmp images sorted by filename; generated slides include preset Chinese copy and publisher branding unless the code is edited.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
