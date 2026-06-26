## Description: <br>
Tencent Hunyuan video API skill for text-to-video, image-to-video, and video stylization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wszhhx](https://clawhub.ai/user/wszhhx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to submit Tencent Cloud Hunyuan video generation jobs, monitor completion, and save generated MP4 outputs and task metadata. <br>

### Deployment Geography for Use: <br>
China (Tencent Cloud ap-guangzhou API region). <br>

## Known Risks and Mitigations: <br>
Risk: Tencent Cloud credentials may be exposed by setup or debugging commands. <br>
Mitigation: Use limited-scope Tencent Cloud keys and avoid commands that print SecretId or SecretKey values. <br>
Risk: Uploaded images, videos, and prompts are processed by Tencent Cloud and may include private or regulated content. <br>
Mitigation: Submit only media whose processing and retention by Tencent Cloud are acceptable for the use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wszhhx/hunyuan-video) <br>
- [Tencent Hunyuan video API overview](https://cloud.tencent.com/document/product/1616/107795) <br>
- [Tencent Hunyuan video console](https://hunyuan.cloud.tencent.com/#/app/videoModel) <br>
- [Tencent Cloud API key management](https://console.cloud.tencent.com/cam/capi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance with command examples; runtime output includes MP4 files and JSON task metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, tencentcloud-sdk-python, and TENCENT_SECRET_ID/TENCENT_SECRET_KEY environment variables.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
