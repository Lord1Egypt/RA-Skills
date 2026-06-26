## Description: <br>
Image processing tool for compression, background removal/replacement, and upscaling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sanford284](https://clawhub.ai/user/Sanford284) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to compress images, remove or replace image backgrounds, and upscale images through JavaScript APIs or CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image files may contain sensitive personal content. <br>
Mitigation: Use the skill on image files you control and avoid highly sensitive personal photos unless the background-removal dependency is trusted for the deployment context. <br>
Risk: Caller-selected output paths can overwrite important files. <br>
Mitigation: Choose explicit output paths, review destination filenames before execution, and avoid writing over originals unless replacement is intended. <br>
Risk: The skill depends on npm image-processing packages. <br>
Mitigation: Install only in environments where the listed npm dependencies are acceptable and have been reviewed for the intended use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Sanford284/image-process) <br>
- [Publisher profile](https://clawhub.ai/user/Sanford284) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write compressed, background-removed, background-replaced, or upscaled image files to caller-selected output paths.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
