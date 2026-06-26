## Description: <br>
Image Resizer resizes, crops, converts, and compresses local images by pixel dimensions, scale, maximum bounds, aspect ratio, output format, quality, or target file size. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and agents use this skill to generate thumbnails, social images, compressed assets, format conversions, and batch-ready resize commands for local image files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the script dependencies fetches npm packages. <br>
Mitigation: Install only in environments where fetching npm dependencies is acceptable, and review the dependency lock state before use when required by policy. <br>
Risk: An explicit output path may overwrite an existing file. <br>
Mitigation: Choose output paths deliberately and avoid naming files that should be preserved. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash commands; the bundled script produces local image files and console status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local input and output paths; explicit output paths can overwrite existing files.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
