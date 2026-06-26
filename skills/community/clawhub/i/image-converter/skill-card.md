## Description: <br>
Converts image files between PNG, JPG, WEBP, SVG, GIF, and BMP formats, including batch conversion and quality-controlled lossy outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to ask an agent to convert individual image files or batches of image files between common formats. It is most useful when local image conversion, output quality control, or folder-based conversion is needed without a network service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads image files or folders selected by the user and writes converted outputs. <br>
Mitigation: Run it only on intended image paths and avoid sensitive or system directories. <br>
Risk: The skill depends on local Python image-processing packages. <br>
Mitigation: Install the dependencies in a virtual environment when stronger package isolation is needed. <br>
Risk: Some format conversions can change image properties, such as losing transparency when converting PNG to JPG. <br>
Mitigation: Keep originals and inspect converted outputs before replacing source files. <br>


## Reference(s): <br>
- [ClawHub Image Converter release page](https://clawhub.ai/tobewin/image-converter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with Python or shell snippets, plus converted image files when executed by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local file input and output, supports batch conversion over user-selected folders, and may apply a quality setting for lossy formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
