## Description: <br>
Converts a configured PowerPoint file on macOS into slide images and thumbnail grids, then creates a WeChat official account draft with the generated images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoxm8023](https://clawhub.ai/user/zhaoxm8023) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators and operators of WeChat official accounts can use this skill to turn a local PPT deck into publishable slide images, thumbnail grids, and a draft article using configured WeChat credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses WeChat app credentials and uploads PPT-derived images to a WeChat official account draft. <br>
Mitigation: Use dedicated or scoped WeChat credentials where possible, avoid storing real secrets in shared config files, and review the draft before public release. <br>
Risk: The conversion and upload flow depends on local file paths and generated PNG contents. <br>
Mitigation: Verify the LibreOffice and Ghostscript paths, keep the output folder free of unrelated PNGs, and confirm the intended PPT before running the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaoxm8023/ppt2wechat) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with configuration values and shell commands; generated files include PNG images, thumbnail grids, and a local Markdown gallery.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local LibreOffice, Ghostscript, Pillow, and valid WeChat official account credentials before creating the WeChat draft.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
