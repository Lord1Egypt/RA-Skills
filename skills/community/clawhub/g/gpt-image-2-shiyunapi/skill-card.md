## Description: <br>
Generates new images and edits supplied images through ShiyunApi's GPT-image-2 image generation and image editing endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gl894761214](https://clawhub.ai/user/gl894761214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create images from text or edit supplied images for posters, avatars, covers, product images, illustrations, background replacement, local repainting, and multi-image composition through ShiyunApi. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to ShiyunApi. <br>
Mitigation: Use the skill only when sharing that content with ShiyunApi is acceptable, and avoid sensitive images or prompts unless approved. <br>
Risk: The key-saving helper can persist SHIYUN_API_KEY in the user's shell profile or Windows user environment. <br>
Mitigation: Use a revocable API key, prefer an existing environment variable or process-scoped storage when possible, and run the helper only when persistent storage is intentional. <br>
Risk: Requests and retries may consume paid quota or create billing impact. <br>
Mitigation: Confirm parameters before execution, monitor quota, and avoid retry variants that may submit another request unless the user accepts the possible charge. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gl894761214/gpt-image-2-shiyunapi) <br>
- [ShiyunApi text-to-image API documentation](https://shiyunapi.apifox.cn/api-448504710) <br>
- [ShiyunApi image editing API documentation](https://shiyunapi.apifox.cn/api-448504709) <br>
- [Bundled ShiyunApi GPT-Image-2 API reference](artifact/references/api_docs.md) <br>
- [Bundled ShiyunApi usage examples](artifact/references/examples.md) <br>
- [Bundled ShiyunApi troubleshooting guide](artifact/references/troubles.md) <br>


## Skill Output: <br>
**Output Type(s):** [Image files, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [PNG, JPEG, WebP, JSON, and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save raw API responses and metadata JSON for troubleshooting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
