## Description:

This skill helps agents use AI Hive's Nano Banana 2 / Gemini Image workflow to normalize same-SKU, multi-angle product photos into a consistent e-commerce studio batch while preserving view-specific product facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce content teams, marketplace operators, and agent developers use this skill to retouch and normalize product listing images across Amazon, Taobao, Tmall, JD, TikTok Shop, Shopify, and similar catalog workflows. It is intended for batch consistency of background, white balance, subject scale, shadow, and finish while protecting SKU, packaging, text, and view-specific product details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed through command-line history or local configuration if handled carelessly.

Mitigation: Prefer AI_HIVE_API_KEY, avoid putting keys directly on the command line, and review local configuration file permissions before use.

Risk: Product photos, packaging text, and other sensitive catalog assets are uploaded to a remote AI Hive service for generation.

Mitigation: Use --preview before generation, run the skill in an isolated environment, and avoid confidential images unless the AI Hive service and its storage redirects are acceptable for the data.

Risk: Generated product images can introduce misleading changes to SKU facts, packaging text, logos, ports, materials, or view-specific details.

Mitigation: Review the output against the declared batch locks, view locks, truth-source images, and acceptance criteria before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-product-retouch)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI Hive OpenAPI root](https://ai-hive.iclip.cn/api/openapi/v1)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls, Files]

**Output Format:** [Markdown guidance with shell commands, JSON preview output, and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses one target image, one approved master image, and one to six truth-source images per frame; preview mode emits the fixed model, reference order, prompt, and params without uploading materials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
