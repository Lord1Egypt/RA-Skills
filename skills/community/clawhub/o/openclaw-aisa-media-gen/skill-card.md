## Description: <br>
Generates images and videos through the AIsa API, using Gemini 3 Pro Image for images and Qwen Wan 2.6 for video tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaimengphp](https://clawhub.ai/user/chaimengphp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative automation users use this skill to generate images from text prompts, create asynchronous video tasks from a reference image, poll task status, and download generated media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, reference image URLs, and generated-media requests to AIsa. <br>
Mitigation: Use it only with data permitted for AIsa, and do not submit secrets or private media unless allowed. <br>
Risk: The skill requires an AISA_API_KEY to call the external service. <br>
Mitigation: Use a revocable key and provide it through environment variables or secure agent secret handling. <br>
Risk: Generated images and downloaded videos are written to user-provided paths. <br>
Mitigation: Review output paths before running commands to avoid overwriting files or placing media in unintended locations. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/chaimengphp/openclaw-aisa-media-gen) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>
- [Gemini GenerateContent documentation](https://docs.aisa.one/reference/generatecontent) <br>
- [Video generation documentation](https://docs.aisa.one/reference/post_services-aigc-video-generation-video-synthesis) <br>
- [Task status documentation](https://docs.aisa.one/reference/get_services-aigc-tasks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API responses; generated media is saved as image or MP4 files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; image output can be PNG, JPEG, or WebP, and video output can be downloaded as MP4.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
