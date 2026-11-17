## Description:

图转视频 Skill，把图片生成短视频，覆盖参考图模式和首尾帧模式，支持 seedance2.0、seedance2.0fast、可灵、HappyHorse、海螺和 wan2.6 等模型路线。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate short videos from one or more image URLs, either by using reference images or by controlling first and optional last frames. It helps route supported model choices, validate video parameters, and return local generated-video paths or user-readable failure guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends image URLs, prompts, account tokens, phone/SMS onboarding data, and billing actions to LinkFox services.

Mitigation: Install and use it only when LinkFox is trusted for those data classes; avoid submitting sensitive or unauthorized images and prompts.

Risk: Long-lived LinkFox API keys may be exposed if stored in shell startup files or shared workspaces.

Mitigation: Prefer session-scoped environment variables or a secrets manager, and rotate keys if they are copied into persistent shell configuration.

Risk: The onboarding flow can create payment QR codes or payment URLs for billing actions.

Mitigation: Treat payment creation as a deliberate user-approved step and verify plan, amount, and payment method before continuing.

Risk: Generated media downloads and local response files may contain user-provided media context or service response details.

Mitigation: Review workspace retention and sharing practices before using the skill with confidential prompts, image URLs, or generated videos.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-aigc-videogen-image-to-video)
- [Image-to-video orchestration API reference](artifact/references/api.md)
- [Image-to-video orchestration test cases](artifact/examples/test-cases.md)
- [Single-image and first/last-frame API reference](artifact/skills/linkfox-aigc-videogen/references/api.md)
- [Multi-reference image API reference](artifact/skills/linkfox-aigc-videogen-multi/references/api.md)
- [Authentication and billing onboarding guidance](artifact/skills/linkfox-aigc-videogen/references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown with JSON parameter examples, shell commands, and generated media paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful runs return local video file paths; failed runs return concise guidance based on the underlying error.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
