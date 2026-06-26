## Description: <br>
Batch-compresses, resizes, and converts local image files with preview and undo workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users working with local image folders use this skill to run a Python image optimizer for batch resizing, compression, and format conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup and undo behavior can write or restore local files outside the expected scope. <br>
Mitigation: Use --preview or --output-dir first, run from a trusted working directory, and avoid --undo in directories containing untrusted .image_optimizer_log.json files. <br>
Risk: Installing dependencies directly with pip can affect the active Python environment. <br>
Mitigation: Install Pillow in an isolated Python environment before running the tool on important folders. <br>


## Reference(s): <br>
- [Image Optimizer Tool on ClawHub](https://clawhub.ai/utopiabenben/image-optimizer-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command examples for installing Pillow and running the image optimizer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
