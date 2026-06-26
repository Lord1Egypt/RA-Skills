## Description: <br>
AI image generation - Generate images using OpenAI DALL-E or other AI image APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukaizj](https://clawhub.ai/user/lukaizj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate images from text prompts, edit existing image files, and create image variations through OpenAI image APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, API requests, and selected image files are sent to OpenAI and may expose sensitive content or incur API charges. <br>
Mitigation: Store OPENAI_API_KEY in a secure environment variable or secret manager, monitor usage, and avoid submitting private prompts or files unless they are intended for OpenAI processing. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/lukaizj/ai-image-skill) <br>
- [OpenAI API key setup](https://platform.openai.com/api-keys) <br>
- [ClawHub listing](https://clawhub.ai/lukaizj/lukaizj-ai-image) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text] <br>
**Output Format:** [JSON objects containing success status, image URL(s), or error text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENAI_API_KEY; image editing and variations may upload selected local image files to OpenAI.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
