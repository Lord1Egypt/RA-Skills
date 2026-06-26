## Description: <br>
Uses a reference KV, poster, or face image with gpt-image-2 or Nano Banana models to batch-generate exact-size image assets and optionally check text cropping and element completeness before delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siconvip](https://clawhub.ai/user/siconvip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and marketing teams use this skill to adapt a source creative image into platform-specific campaign assets for social, content, and commerce channels. It supports batch output, custom platform sizes, quality options, optional AI self-checks, and cloud handoff through JSON or base64 image payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded images and prompts may be sent to remote AI services. <br>
Mitigation: Process only assets approved for the configured service, and verify the configured base_url before using confidential or licensed material. <br>
Risk: The skill requires sensitive API credentials. <br>
Mitigation: Prefer environment-variable API keys and avoid storing plaintext keys in local configuration files or shared workspaces. <br>
Risk: Optional native software download and external helper execution can introduce unreviewed code. <br>
Mitigation: Avoid the Real-ESRGAN install path and default external gpt_image2.py helper unless the files and sources have been independently verified. <br>


## Reference(s): <br>
- [Platform image specifications](references/platform-specs.md) <br>
- [ClawHub skill page](https://clawhub.ai/siconvip/image-assets-resize) <br>
- [OpenClaw homepage](https://github.com/openclaw/clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [PNG image files with JSON status objects; cloud mode can include base64-encoded image data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an input image, target platform dimensions, and API credentials for the selected image model.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
