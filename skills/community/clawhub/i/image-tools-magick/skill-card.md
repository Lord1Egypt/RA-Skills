## Description: <br>
Comprehensive ImageMagick toolkit for resizing, cropping, compositing, padding, annotating, adjusting, removing solid backgrounds, converting formats, and inspecting images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pratiknarola](https://clawhub.ai/user/pratiknarola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform local pixel-level image operations through ImageMagick shell helpers while writing results to new files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted image-editing parameters may trigger unintended shell commands in helpers that build commands through eval. <br>
Mitigation: Review before installing, use only trusted inputs, and avoid untrusted annotation text, paths, colors, offsets, rotation, blur, sharpen, and border values until helpers use safely quoted argument arrays and basic option validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pratiknarola/image-tools-magick) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for non-destructive image transformations that write outputs to new files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
