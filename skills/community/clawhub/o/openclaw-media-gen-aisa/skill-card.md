## Description: <br>
Openclaw Media Gen helps agents generate images and videos through AIsa using one API key and a bundled Python client that routes supported models to the right endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create AI-generated images and videos from text prompts or reference image URLs through AIsa-supported models. It is useful when an agent workflow needs media generation, task polling, and local download of generated media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, model selections, reference image URLs, and API-key usage are sent to AIsa external services. <br>
Mitigation: Install only if AIsa is trusted for the workflow, and avoid sending secrets, internal URLs, regulated content, or proprietary material unless approved. <br>
Risk: Generated media downloads can write to user-selected output paths, including paths where files already exist. <br>
Mitigation: Review output paths before execution and prefer a dedicated output directory for generated images and videos. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baofeng-tech/openclaw-media-gen-aisa) <br>
- [AIsa homepage](https://aisa.one) <br>
- [AIsa API reference](https://aisa.one/docs/api-reference) <br>
- [Google Gemini Chat generateContent](https://aisa.one/docs/api-reference/chat/generatecontent) <br>
- [Image Generation via Chat](https://aisa.one/docs/api-reference/chat/image-generation) <br>
- [OpenAI-Compatible Image Generations](https://aisa.one/docs/api-reference/chat/openai-image-generations) <br>
- [Create video generation task](https://aisa.one/docs/api-reference/video/post_services-aigc-video-generation-video-synthesis) <br>
- [Get video generation task result](https://aisa.one/docs/api-reference/video/get_services-aigc-tasks) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Files, Configuration] <br>
**Output Format:** [Markdown guidance with bash commands and JSON responses; generated media is saved as image or MP4 files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and Python 3. User-selected output paths may be overwritten by generated media downloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
