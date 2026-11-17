## Description:

用户指定 GPT Image 2.6 / 智慧模型2.6，制作电商促销海报、活动主视觉、节日营销图或折扣海报时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商运营人员和设计师可用此技能为促销、节日和折扣活动制作营销海报及多版位视觉素材，并根据确认过的活动信息安排版面。

### Deployment Geography for Use:

China (the workflow uses Qinghu's CN service).

## Known Risks and Mitigations:

Risk: Reference images are uploaded to Qinghu during generation.

Mitigation: Use only reference images you are comfortable uploading.

Risk: Generation can incur charges and depends on the active account and service address.

Mitigation: Verify the account and service address, review the quoted cost, and confirm sufficient balance before generation.

Risk: The API key could be exposed if included in task data or replies.

Mitigation: Protect the key and provide it through the process environment; do not include it in task JSON or replies.

Risk: The workflow may install the latest qhkit CLI globally, and that external dependency was outside the artifact review.

Mitigation: Review the external package and release before installing it.

Risk: Generated artwork may render exact prices, long terms, or QR codes inaccurately or illegibly.

Mitigation: Leave space for these elements, add confirmed copy and assets locally, and check dates, discounts, and readability.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/linkpix-gpt-image-2-6-promo-poster)

## Skill Output:

**Output Type(s):** [Images, Text, Guidance, Configuration, Shell commands]

**Output Format:** [Generated image files with Markdown guidance and JSON parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image count, size, and quality depend on the model options returned at runtime; prompts are limited to 5,000 characters.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
