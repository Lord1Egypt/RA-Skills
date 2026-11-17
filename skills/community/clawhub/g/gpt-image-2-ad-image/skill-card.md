## Description:

使用 GPT Image 2 制作以点击、加购、留资或转化为目标的广告图片，并围绕受众、卖点、证据、优惠和构图建立可归因的A/B测试。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers, advertisers, ecommerce operators, and developers use this skill to brief and generate GPT Image 2 ad-image concepts for performance campaigns, including feed ads, remarketing images, product evidence visuals, and single-variable A/B creative tests. The skill emphasizes approved product facts, clear composition, attribution-ready test variables, and platform review before launch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The init flow stores an AI Hive API key locally in ~/.ai-hive/config.json.

Mitigation: Use a normal user account or virtual environment, keep the config file private, rotate keys when needed, and prefer environment variables for short-lived use.

Risk: Reference images and uploaded media are sent to AI Hive for generation.

Mitigation: Upload only files that are intended for AI Hive processing and confirm usage rights for product, person, trademark, and campaign assets before submission.

Risk: Generated ad visuals can imply unapproved claims, offers, certifications, ratings, or legal text.

Mitigation: Keep price, terms, dates, ratings, certifications, and legal copy tied to approved source files, then review the final creative against current platform policies before launch.

Risk: Dependency behavior may vary if requests is installed without pinned versions.

Mitigation: Pin dependencies in the consuming environment when reproducibility matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/gpt-image-2-ad-image)
- [AI Hive API access](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, files]

**Output Format:** [Markdown guidance with bash commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports prompts, reference images, batch size, model parameters, routing mode, output directory selection, task polling, and optional no-download task submission.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
