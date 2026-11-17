## Description:

把商品图、卖点、销售地区、受众、语言和时长组装成跨境电商带货口播 MP4，覆盖商品口播、TikTok 带货视频、达人种草视频和 e-commerce talking head video。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, ecommerce sellers, and their agents use this skill to turn product images and selling points into localized short-form sales videos. It prepares three structured talking-video concepts for user selection, then composes the final video prompt and delegates MP4 generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images, prompts, account identifiers, and payment/onboarding data may be sent to LinkFox services.

Mitigation: Install only when that data sharing is acceptable, and avoid submitting sensitive, unauthorized, or regulated content.

Risk: Custom LINKFOX_* endpoint environment variables may change where requests are sent.

Mitigation: Use custom endpoint variables only when the destination is fully trusted.

Risk: API keys and account/payment steps are part of the workflow.

Mitigation: Avoid storing API keys in shell startup files and review any plan, order, or payment step before proceeding.

Risk: Hard-coded demographic casting rules may be unsuitable for compliant creative work.

Mitigation: Remove or override demographic casting rules when compliance, fairness, or customer policy requires it.

Risk: Generated media is downloaded locally and failed responses can be written as JSON files.

Mitigation: Return only the local media paths or user-readable error summaries; do not expose raw video contents, base64 data, or temporary source URLs.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-aigc-videogen-sale)
- [Skill workflow](artifact/SKILL.md)
- [Business parameter and routing reference](artifact/references/api.md)
- [Prompt construction reference](artifact/references/prompt.md)
- [Call examples](artifact/references/call-examples.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Test cases](artifact/examples/test-cases.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, files]

**Output Format:** [Markdown guidance, structured JSON parameters, and local MP4 media paths from delegated video generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Two-stage interaction: the agent presents three candidate schemes, waits for user selection, then returns local video paths when generation succeeds.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
