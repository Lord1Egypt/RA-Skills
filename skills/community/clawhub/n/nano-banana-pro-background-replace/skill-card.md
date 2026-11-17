## Description:

Uses Nano Banana Pro through AI Hive to remove, replace, and extend image backgrounds for products or people while preserving subject identity and scene consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce teams, advertisers, and developers use this skill to guide Nano Banana Pro background replacement workflows for product images, portraits, lifestyle scenes, and localized ad variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key can be sent to any configured base URL.

Mitigation: Use the default AI Hive endpoint unless a custom endpoint is fully trusted, and use a dedicated low-privilege API key.

Risk: Selected source images are uploaded to AI Hive for generation tasks.

Mitigation: Avoid sensitive images unless upload is approved, and confirm rights or consent for product, brand, and person images.

Risk: Generated background replacements can unintentionally change product facts, identity, logos, colors, or other subject details.

Mitigation: Compare outputs against the source image and keep the original plus generated versions as an audit record.

Risk: The skill runs networked Python code with a third-party dependency.

Mitigation: Run it in an isolated virtual environment and pin or review the requests dependency before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-pro-background-replace)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples; the CLI returns status text or JSON and can download generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured AI Hive API key, optional reference images, batch size, routing mode, and output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact changelog top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
