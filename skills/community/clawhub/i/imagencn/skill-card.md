## Description:

Multi-platform AI image generation via DashScope/Ark/Hunyuan/Zhipu/StepFun, specializing in Chinese text rendering and photorealistic images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to refine prompts, choose a Chinese-capable image model, and generate or edit images through supported provider APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, input images, and API credentials may be sent to external image-generation providers.

Mitigation: Use dedicated low-privilege API keys and avoid submitting sensitive prompts, images, or secrets.

Risk: A user-configured DashScope endpoint may route requests outside the expected provider endpoint set.

Mitigation: Keep DASHSCOPE_API_BASE set to cn, sg, us, or a trusted HTTPS Aliyun endpoint.

Risk: Runtime dependencies and provider clients can affect the execution environment.

Mitigation: Install in a virtual environment with reviewed pinned dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agents365-ai/skills/imagencn)
- [DashScope API endpoints](https://dashscope.aliyuncs.com/api/v1)
- [Tencent Hunyuan image generation endpoint](https://api.hunyuan.cloud.tencent.com/v1/images/generations)
- [Volcano Ark image generation endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations)
- [Zhipu image generation endpoint](https://api.z.ai/api/paas/v4/images/generations)
- [StepFun image generation endpoint](https://api.stepfun.com/v1/images/generations)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, files, JSON]

**Output Format:** [Markdown guidance with bash commands; generated image files; optional JSON status envelopes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires provider API credentials and writes image outputs to the requested or generated file path.]

## Skill Version(s):

1.7.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
