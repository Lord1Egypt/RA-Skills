## Description:

Nano Banana Pro 产品图生成 helps agents create brand-consistent product photography sets for catalogs, ecommerce listings, lifestyle scenes, detail shots, bundles, color SKUs, and launch assets using AI Hive reference-image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants, ecommerce operators, and creative teams use this skill to plan product DNA and generate consistent AI product photos from approved reference media for marketplace, social commerce, and storefront channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an AI Hive API key locally and accepts a configurable API base URL, so credentials could be exposed if an untrusted endpoint is used.

Mitigation: Use the default HTTPS AI Hive endpoint, avoid unknown or HTTP base URLs, and keep the local config file permissions restricted.

Risk: Selected reference product media is uploaded to AI Hive for generation tasks.

Mitigation: Review media before upload and avoid submitting confidential or rights-restricted assets unless approved for that service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-pro-product-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, image files]

**Output Format:** [Markdown guidance with bash command examples, CLI status text, JSON task details, and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses approved reference media and prompt recipes; generated PNG results are downloaded unless no-download mode is selected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
