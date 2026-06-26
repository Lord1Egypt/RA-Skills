## Description: <br>
Resize images using ImageMagick (CLI). Entrypoint is a Bash script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pr1vateer](https://clawhub.ai/user/pr1vateer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and agents working with local image assets use this skill to resize images through ImageMagick from a shell command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The resize command writes image files and can create an output directory specified by the caller. <br>
Mitigation: Review input and output paths before execution and run the command in the intended workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pr1vateer/image-magik-resize) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [Resized image file with terminal status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to the provided output path, or creates an input-resized file next to the source image when no output path is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact frontmatter says 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
