## Description: <br>
AI image generation in any visual style, including photorealistic, cinematic, cartoon, illustration, and more, with support for transforming photos or generating from text prompts through the Pop-cam NanoBanana API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[petagit](https://clawhub.ai/user/petagit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create images from prompts or transform user-provided images through the Pop-cam NanoBanana API. It supports synchronous generation and webhook-based asynchronous workflows when an HTTPS callback endpoint is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and source images are sent to Pop-cam for generation. <br>
Mitigation: Use the skill only when the user is comfortable sharing that content with Pop-cam. Avoid sending sensitive images or prompts unless the user has approved the disclosure. <br>
Risk: The POPCAM_API_TOKEN can spend Pop-cam credits. <br>
Mitigation: Keep the token private, pass it through the declared environment variable, and avoid exposing it in logs, prompts, or shared files. <br>
Risk: Webhook delivery can send generated-image results to a callback URL. <br>
Mitigation: Use only HTTPS webhook URLs that the user controls and trusts, or omit webhook_url for synchronous operation. <br>


## Reference(s): <br>
- [Pop-cam OpenClaw homepage](https://www.pop-cam.com/openclaw) <br>
- [Pop-cam OpenClaw skill definition](https://www.pop-cam.com/api/openclaw/skill) <br>
- [ClawHub skill page](https://clawhub.ai/petagit/pop-cam) <br>
- [Publisher profile](https://clawhub.ai/user/petagit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POPCAM_API_TOKEN and curl for API requests; generation responses include job metadata and image download URLs.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
