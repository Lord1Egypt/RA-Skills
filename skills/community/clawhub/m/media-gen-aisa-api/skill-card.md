## Description: <br>
Generate images and videos with AIsa using one API key, with a bundled client that routes supported image and video models to the correct endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate images, submit asynchronous video jobs, poll task status, and download completed media through AIsa. It is useful when a workflow needs a single CLI-oriented interface across Gemini image, Wan image, Seedream, and Wan video models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference image URLs are sent to AIsa using the configured API key. <br>
Mitigation: Avoid confidential prompts, secrets, internal-only URLs, or sensitive media unless sharing them with AIsa is intended. <br>
Risk: Generated media downloads can overwrite local files when an output path is reused. <br>
Mitigation: Choose output paths deliberately and review existing files before downloading generated results. <br>
Risk: AISA_API_KEY is a sensitive credential required for API calls. <br>
Mitigation: Provide the key through the environment or command-line only in trusted sessions and avoid committing it to files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bibaofeng/media-gen-aisa-api) <br>
- [AIsa API Reference](https://aisa.one/docs/api-reference) <br>
- [Google Gemini Chat generateContent](https://aisa.one/docs/api-reference/chat/generatecontent) <br>
- [Image Generation via Chat](https://aisa.one/docs/api-reference/chat/image-generation) <br>
- [OpenAI-Compatible Image Generations](https://aisa.one/docs/api-reference/chat/openai-image-generations) <br>
- [Create Video Generation Task](https://aisa.one/docs/api-reference/video/post_services-aigc-video-generation-video-synthesis) <br>
- [Get Video Generation Task Result](https://aisa.one/docs/api-reference/video/get_services-aigc-tasks) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated media is saved as image or video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and Python 3; video generation uses asynchronous task polling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
