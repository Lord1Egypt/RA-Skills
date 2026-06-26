## Description: <br>
Convert HTML and CSS into PNG images via Chrome headless for accurate text layouts such as covers, posters, and info cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuhedev](https://clawhub.ai/user/liuhedev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content creators use this skill to turn local HTML and CSS layouts into PNG images with Chrome or Chromium headless screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted HTML can render unwanted or misleading content during screenshot capture. <br>
Mitigation: Use trusted local HTML files and review layouts in a regular browser before generating the final image. <br>
Risk: Screenshot output paths can overwrite existing files. <br>
Mitigation: Choose output paths deliberately and confirm the destination before running Chrome headless. <br>
Risk: A custom CHROME_PATH can point the agent to an unexpected executable. <br>
Mitigation: Use a trusted Chrome or Chromium installation and do not set CHROME_PATH to an unknown executable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liuhedev/lh-html-to-image) <br>
- [Skill homepage](https://github.com/liuhedev/lh-openclaw-kit) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with HTML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local HTML inputs and PNG screenshots; image dimensions depend on the Chrome window size and device scale factor.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
