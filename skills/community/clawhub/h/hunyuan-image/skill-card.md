## Description:

腾讯混元生图API，可根据文本描述生成AI图像。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wszhhx](https://clawhub.ai/user/wszhhx)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to generate images with Tencent Hunyuan from text prompts, optional style and resolution settings, and Tencent Cloud credentials.

### Deployment Geography for Use:

Global, with Tencent Cloud API calls routed to ap-guangzhou as documented by the skill.

## Known Risks and Mitigations:

Risk: Prompts and any reference material are sent to Tencent Cloud for image generation.

Mitigation: Avoid sensitive prompts or proprietary reference material, and review Tencent Cloud data handling terms before use.

Risk: The skill requires Tencent Cloud credentials in environment variables.

Mitigation: Use a dedicated, least-privileged Tencent Cloud key and run the skill in an isolated Python environment.

Risk: The artifact includes guidance that appears to work around provider content filters.

Mitigation: Do not rely on content-filter workaround guidance; follow provider policy and review prompts before execution.

Risk: Generated images and info.json metadata are stored locally.

Mitigation: Store outputs in an appropriate location, restrict access as needed, and review metadata before sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wszhhx/skills/hunyuan-image)
- [Tencent Hunyuan Image API Documentation](https://cloud.tencent.com/document/product/1729/105969)
- [Tencent Cloud API Key Console](https://console.cloud.tencent.com/cam/capi)
- [Tencent Hunyuan Image Style List](https://cloud.tencent.com/document/product/1729/105846)

## Skill Output:

**Output Type(s):** [Files, Images, JSON, Shell commands, Guidance]

**Output Format:** [PNG image files, info.json metadata, and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud credentials and saves outputs under {output}/{date}/{job_id}/.]

## Skill Version(s):

1.0.3 (source: server release metadata and package.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
