## Description: <br>
Resize images using ImageMagick from a Bash command-line entrypoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pr1vateer](https://clawhub.ai/user/pr1vateer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to resize local image files with ImageMagick, including fixed-width, exact-geometry, percentage, and conditional resizing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Processing images from untrusted sources can expose ImageMagick parsing vulnerabilities if ImageMagick is outdated. <br>
Mitigation: Keep ImageMagick updated and avoid processing untrusted images unless the execution environment is appropriately isolated. <br>
Risk: The skill writes resized images to an explicit or default local output path. <br>
Mitigation: Review the input and output paths before execution and run the skill with filesystem permissions appropriate for the working directory. <br>


## Reference(s): <br>
- [ClawHub skill release: Image Magic resizer](https://clawhub.ai/pr1vateer/image-resize) <br>
- [Publisher profile: pr1vateer](https://clawhub.ai/user/pr1vateer) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, guidance] <br>
**Output Format:** [Shell command execution with text status output and resized image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and either magick or convert from ImageMagick.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
