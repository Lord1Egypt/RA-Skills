## Description: <br>
腾讯混元生图API - 根据文本描述生成AI图像 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wszhhx](https://clawhub.ai/user/wszhhx) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to generate image files from text prompts through Tencent Cloud Hunyuan, configure generation options, and save generated images plus job metadata locally. <br>

### Deployment Geography for Use: <br>
Tencent Cloud Hunyuan API region: ap-guangzhou. <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Tencent Cloud credentials and can use those credentials to submit image-generation jobs. <br>
Mitigation: Use a least-privileged Tencent Cloud key, store it only in environment variables or an approved secrets manager, and rotate it if exposed. <br>
Risk: Prompts, job metadata, and generated output may be processed by Tencent Cloud and saved locally in info.json and image files. <br>
Mitigation: Avoid sensitive or regulated text in prompts, review outputs before sharing, and protect or delete local output directories when they are no longer needed. <br>
Risk: The artifact documentation includes prompt-rewording advice that could be used to work around provider content filters. <br>
Mitigation: Follow Tencent Cloud acceptable-use requirements and do not use prompt rewording to evade safety or content restrictions. <br>


## Reference(s): <br>
- [腾讯混元生图 API 文档](https://cloud.tencent.com/document/product/1729/105969) <br>
- [腾讯云 API 密钥控制台](https://console.cloud.tencent.com/cam/capi) <br>
- [腾讯混元生图风格列表](https://cloud.tencent.com/document/product/1729/105846) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Images, JSON, Shell commands, Guidance] <br>
**Output Format:** [PNG image files, JSON job metadata, and markdown usage guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud credentials; saves outputs under {output}/{date}/{job_id}/; submits asynchronous jobs to ap-guangzhou.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and package.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
