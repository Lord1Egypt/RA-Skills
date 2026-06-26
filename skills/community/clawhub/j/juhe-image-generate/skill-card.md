## Description: <br>
Generates AI images from text prompts through Juhe Data's text-to-image API, supports common aspect ratios, and can download generated images locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create images from natural-language prompts, select an aspect ratio for the intended medium, and return a temporary image link plus an optional local file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: JUHE_IMAGE_KEY can be exposed if passed on the command line or stored in a poorly protected .env file. <br>
Mitigation: Prefer an environment variable or secret manager, avoid command-line key arguments, do not commit scripts/.env, and restrict local file permissions. <br>
Risk: Generated image links are temporary and may stop working after the documented 24-hour validity window. <br>
Mitigation: Download required images promptly and keep the local saved file when durable access is needed. <br>
Risk: Image generation depends on the external Juhe API and may fail or time out. <br>
Mitigation: Handle API errors as user-visible failures and retry later or adjust the prompt when the service reports generation or content issues. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/juhe-image-generate) <br>
- [Juhe AI image generation API documentation](https://www.juhe.cn/docs/api/id/824) <br>
- [Juhe text-to-image API endpoint](https://gpt.juhe.cn/text2image/generate) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration] <br>
**Output Format:** [Plain text with command examples, generated image URLs, and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUHE_IMAGE_KEY; generated image links are described as valid for 24 hours.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
