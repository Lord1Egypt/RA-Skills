## Description: <br>
High quality AI image generation via the WellAPI gpt-image-2 model. Supports text-to-image and image editing (image-to-image). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laolujava](https://clawhub.ai/user/laolujava) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw-compatible agent generate new images from prompts or edit local images through WellAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, the WellAPI API key, and selected image or mask files are sent to a third-party API. <br>
Mitigation: Use the skill only for content approved for WellAPI processing, and avoid confidential, regulated, or proprietary inputs unless that transfer is authorized. <br>
Risk: High-quality or large image renders may consume paid WellAPI quota. <br>
Mitigation: Start with lower quality or smaller draft renders, then request high-quality or 4K output only for final images. <br>
Risk: Generated image files are written to local storage and announced through MEDIA path lines. <br>
Mitigation: Review output paths and apply local retention or cleanup controls appropriate for the workspace. <br>
Risk: Unsanitized output filenames could be unsafe if passed to shell commands. <br>
Mitigation: Use the documented filename sanitization and extension whitelist before shell interpolation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/laolujava/image-generation-gpt) <br>
- [Publisher Profile](https://clawhub.ai/user/laolujava) <br>
- [WellAPI](https://wellapi.ai) <br>
- [Skill Manifest](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Python Reference Implementation](artifact/references/python.md) <br>
- [PowerShell Reference Implementation](artifact/references/powershell.md) <br>
- [curl and Bash Reference Implementation](artifact/references/curl_heredoc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, API Calls] <br>
**Output Format:** [Generated PNG, JPEG, or WebP image files plus MEDIA:<absolute_path> text lines.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Images are decoded from base64 responses and saved locally with sanitized wellapi-<timestamp> filenames.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and changelog list 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
