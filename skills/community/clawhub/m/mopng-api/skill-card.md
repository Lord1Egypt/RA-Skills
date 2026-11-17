## Description:

通过 qise-studio/motu-agent 的 MoPNG Agent OpenAPI 协商完成图片生成与修图。适用于文生图、图生图、抠图、换背景、扩图、放大及多步图像工作流；技能负责把用户需求转成 Brief、审阅/修订 Plan、批准执行并交付结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkin8010](https://clawhub.ai/user/jkin8010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agents use this skill to turn image-generation and editing requests into a proposed plan, negotiate revisions, and deliver generated image links or text results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills.

Mitigation: Review and scan skill before deployment.

## Reference(s):

- [Source repository](https://github.com/jkin8010/mopng-api)
- [Server-resolved source commit](https://github.com/jkin8010/mopng-api/commit/093ae39b1b7c564b68b271f6a26373b4d9386e46)
- [ClawHub release page](https://clawhub.ai/jkin8010/skills/mopng-api)

## Skill Output:

**Output Type(s):** [Guidance, Text, Image URLs]

**Output Format:** [Generated image links or text results with plan and execution summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include plan details, service-reported cost and time estimates, execution status, and result links.]

## Skill Version(s):

0.1.9 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
