## Description: <br>
Generates or edits images with Google's Gemini 3.1 Flash Image Preview API, supporting text-to-image, image-to-image, and 1K, 2K, or 4K output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative agents use this skill to generate new PNG images or edit existing images from natural-language prompts through Google's Gemini image API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and optional input images are sent to Google's Gemini service for processing. <br>
Mitigation: Avoid confidential, regulated, proprietary, or personal images unless that external processing is approved. <br>
Risk: The skill requires a Gemini API key supplied by argument or the GEMINI_API_KEY environment variable. <br>
Mitigation: Use approved secret-handling practices, avoid committing keys, and rotate keys if they are exposed. <br>
Risk: The artifact installs Python dependencies through uv without pinned exact versions. <br>
Mitigation: Pin and review dependencies in managed or production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/franklu0819-lang/nano-banana-2-direct) <br>
- [Publisher profile](https://clawhub.ai/user/franklu0819-lang) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated PNG file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves PNG files to the user's current working directory or specified output path; supports 1K, 2K, and 4K resolution settings.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
