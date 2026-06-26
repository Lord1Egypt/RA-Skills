## Description: <br>
Generate and edit images using Google's Nano Banana 2 (Imagen) model with Atlas Cloud or Google AI Studio, including text-to-image generation and image editing with up to 14 reference images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixihhhh](https://clawhub.ai/user/xixihhhh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creative teams use this skill to generate new images, edit existing images, create visual assets, and produce provider-specific commands or code for Atlas Cloud and Google AI Studio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected images are sent to Atlas Cloud or Google AI Studio for generation or editing. <br>
Mitigation: Use only the provider key you intend to use, and avoid private or confidential prompts or images unless third-party processing is acceptable. <br>
Risk: Editing through Atlas Cloud can upload local files to temporary provider storage. <br>
Mitigation: Require explicit user confirmation before uploading any local image file and use only images approved for provider processing. <br>
Risk: Provider API calls can create billing exposure. <br>
Mitigation: Monitor API usage and provider pricing before running repeated or high-resolution generation jobs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xixihhhh/nano-banana-2-skill) <br>
- [Atlas Cloud](https://www.atlascloud.ai) <br>
- [Google AI Studio API keys](https://aistudio.google.com/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash, curl, and Python snippets; generated or edited images are saved as local files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ATLASCLOUD_API_KEY or GEMINI_API_KEY; Atlas Cloud generation uses asynchronous polling, while Google AI Studio returns base64 image data synchronously.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
