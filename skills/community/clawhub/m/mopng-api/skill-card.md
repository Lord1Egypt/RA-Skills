## Description: <br>
使用 mopng.cn (MoPNG) API 进行图片处理，包括智能抠图、高清放大、智能扩图、图片翻译、文生图、图生图等功能。支持 API Key 鉴权；处理本地文件时会上传至 MoPNG 服务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkin8010](https://clawhub.ai/user/jkin8010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creative operators, and external users use this skill to invoke MoPNG image APIs from agent workflows for background removal, upscaling, outpainting, image translation, text-to-image generation, image-to-image editing, and model listing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images and generation or editing prompts are sent to MoPNG for processing. <br>
Mitigation: Avoid sensitive images or prompts unless the user accepts MoPNG handling policies. <br>
Risk: The MoPNG API key can consume account credits and may be exposed if pasted into conversations or public files. <br>
Mitigation: Store MOPNG_API_KEY only in private client, host, or local environment configuration. <br>
Risk: Raw main-branch install URLs can change outside the reviewed release. <br>
Mitigation: Prefer the reviewed ClawHub release or a pinned source when installing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jkin8010/mopng-api) <br>
- [MoPNG API documentation](https://mopng.cn/agent/docs) <br>
- [MoPNG API key portal](https://mopng.cn/agent) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Image files with text status output and MEDIA paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated or processed images under outputs/mopng-api; requires MOPNG_API_KEY and may consume MoPNG account credits.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release metadata; artifact _meta.json and pyproject.toml list 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
