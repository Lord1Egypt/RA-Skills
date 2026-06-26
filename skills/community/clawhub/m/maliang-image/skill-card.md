## Description: <br>
Generate images from text prompts or edit existing images with AI, powered by Google Gemini via the Maliang API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xexojay](https://clawhub.ai/user/xexojay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate images from prompts or edit user-selected reference images through the Maliang API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected images are sent to the third-party Maliang API. <br>
Mitigation: Use the skill only with prompts and images the user is comfortable sending to nano.djdog.ai. <br>
Risk: The Maliang API key can spend service balance if exposed. <br>
Mitigation: Store MALIANG_API_KEY as a secret, avoid printing it in logs, and revoke or reprovision it if exposure is suspected. <br>
Risk: Large or excessive reference images can fail the edit endpoint. <br>
Mitigation: Check that each decoded image is under 10 MB and send no more than 10 images, as the artifact guardrails require. <br>


## Reference(s): <br>
- [Maliang API homepage](https://nano.djdog.ai) <br>
- [ClawHub skill page](https://clawhub.ai/xexojay/maliang-image) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with API commands, status summaries, image URLs, or saved file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return a hosted image URL or a local file path when only base64 image data is available.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
