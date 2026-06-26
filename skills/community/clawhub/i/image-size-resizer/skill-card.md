## Description: <br>
Resizes local image files to custom or preset dimensions, with support for batch resizing and preserving aspect ratio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and automation agents use this skill to resize one or more local images to specific dimensions, common social media presets, or constrained width and height while optionally preserving aspect ratio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch resizing can read every supported image in the selected input directory and write resized copies to an output directory. <br>
Mitigation: Limit agent access to only the image files or folders intended for resizing and review output paths before execution. <br>
Risk: The skill depends on Python and Pillow to process local image files. <br>
Mitigation: Install Pillow only in a trusted environment and keep dependencies maintained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobewin/image-size-resizer) <br>
- [Publisher profile](https://clawhub.ai/user/tobewin) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python code and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce resized image files when executed by an agent with access to the selected input and output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
