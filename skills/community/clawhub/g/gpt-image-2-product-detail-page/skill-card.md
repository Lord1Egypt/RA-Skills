## Description:

Guides agents to plan buyer-question-driven ecommerce product detail page modules and generate GPT Image 2 image assets through AI Hive for PDPs, marketplace detail pages, Amazon A+ content, Shopify listings, product selling-point images, infographics, and listing modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, ecommerce operators, and content production teams use this skill to turn approved product evidence into modular product detail page image-generation prompts and runnable AI Hive commands. It is aimed at PDP, marketplace long-image, Amazon A+, Shopify, and listing-module workflows where claims, prices, dimensions, and legal copy must stay grounded in approved source material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real AI Hive API key can be sent to a configurable API host if AI_HIVE_BASE_URL or ~/.ai-hive/config.json is changed.

Mitigation: Use only the default AI Hive base URL and check environment and config-file settings before running the skill with production credentials.

Risk: Reference product files are uploaded to the AI Hive service during generation.

Mitigation: Review uploaded assets for confidential or regulated content and use only files approved for that external service.

Risk: Installing dependencies from an untrusted pip mirror can introduce supply-chain exposure.

Mitigation: Install requests from a trusted Python package index or a vetted internal mirror.

## Reference(s):

- [AI Hive API base URL](https://ai-hive.iclip.cn/api)
- [AI Hive API key help](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline bash commands and generated image-file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses reference product images and AI Hive API credentials; final page assembly and approved copy placement happen outside the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
