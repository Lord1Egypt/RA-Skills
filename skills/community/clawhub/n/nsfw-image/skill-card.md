## Description: <br>
Generates or edits adult-only mature creative images through Atlas Cloud image models with API-key setup, model selection guidance, and a bundled Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixihhhh](https://clawhub.ai/user/xixihhhh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Adults and developers use this skill to generate or edit mature creative imagery for legitimate adult artistic and professional projects, including figure drawing, fashion photography, fine art, and mature illustration. The skill helps an agent select Atlas Cloud image models, configure parameters, upload optional reference images, poll generation jobs, and save generated files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Adult-content image generation is not appropriate for minors or users who have not confirmed they are 18 or older. <br>
Mitigation: Confirm the user is 18 or older before use and refuse execution when age confirmation is not provided. <br>
Risk: Prompts and selected image inputs are sent to Atlas Cloud for generation or editing. <br>
Mitigation: Use only prompts and images the user is allowed and willing to send to Atlas Cloud; avoid confidential or unauthorized images. <br>
Risk: The Atlas Cloud API key can spend from the associated account balance. <br>
Mitigation: Use a dedicated low-balance API key, monitor usage, and revoke the key when finished. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xixihhhh/nsfw-image) <br>
- [Skill-Declared Source Repository](https://github.com/AtlasCloudAI/nano-banana-2-skill) <br>
- [Atlas Cloud](https://www.atlascloud.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ATLASCLOUD_API_KEY and sends prompts or selected image inputs to Atlas Cloud.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
