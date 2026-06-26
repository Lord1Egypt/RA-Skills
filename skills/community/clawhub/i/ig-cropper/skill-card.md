## Description: <br>
Transforms cluttered Instagram mobile screenshots into clean, distraction-free architectural and design reference images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yfxa](https://clawhub.ai/user/yfxa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, architects, and agents building visual reference archives use IG Cropper to crop Instagram mobile screenshots into clean image files while preserving the photographed content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script writes to a user-chosen output path and may overwrite an existing file. <br>
Mitigation: Choose an output filename deliberately and avoid pointing it at files that should be preserved. <br>
Risk: The skill depends on Pillow from the Python package ecosystem. <br>
Mitigation: Install Pillow from a trusted package index without elevated privileges. <br>
Risk: The cropper is tuned for Instagram mobile screenshots in dark mode and may not crop unrelated images as expected. <br>
Mitigation: Use it on screenshots intended for this workflow and review the resulting image before adding it to a reference archive. <br>


## Reference(s): <br>
- [IG Cropper on ClawHub](https://clawhub.ai/yfxa/ig-cropper) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with an inline shell command; the script writes an output image file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and Pillow; reads one input image path and writes one output image path.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
