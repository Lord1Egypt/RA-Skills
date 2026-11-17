## Description:

Guides the creation of multilingual TikTok product and advertising videos using Qinghu AI, from model selection and cost estimates to generation and delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Cross-border sellers, marketing teams, and agencies use this skill to plan and produce short-form TikTok Shop and TikTok Ads videos with localized narration and product imagery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading the external qhkit package introduces dependency risk.

Mitigation: Review the package and prefer a controlled, pinned dependency environment before installing it.

Risk: Setup requires an API key, and generation uploads product media to the provider.

Mitigation: Protect the key and upload only media authorized for sharing with the provider.

Risk: Submitting a video task spends credits and cannot be cancelled.

Mitigation: Confirm model, duration, language, reference files, and estimated credit cost with the user before submission.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-tiktok-viral-video)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu AI API key setup](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with command examples and generated-video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends a model and estimated credits before submission; reports the task ID, completed video link, and charged credits when available.]

## Skill Version(s):

0.1.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
