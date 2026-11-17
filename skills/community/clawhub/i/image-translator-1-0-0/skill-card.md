## Description:

Translate text and images between multiple languages using Xiangji/Tosoiot translation APIs and engines including Baidu, Google, DeepL, ChatGPT, and Aliyun.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcdentoncore](https://clawhub.ai/user/jcdentoncore)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to translate text, translate text embedded in local images, and batch translate image URLs across supported language pairs. It is useful when an agent needs command examples, parameter guidance, or helper scripts for Xiangji/Tosoiot translation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text, images, image URLs, and translation-service keys are sent to third-party Xiangji/Tosoiot translation endpoints.

Mitigation: Use only approved content, avoid regulated or confidential material unless permitted, and confirm that third-party processing is acceptable for the deployment context.

Risk: API credentials can be exposed when pasted directly into shell commands, logs, or CI output.

Mitigation: Pass credentials through environment variables, secret stores, or a local wrapper that avoids command history and log disclosure.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jcdentoncore/skills/image-translator-1-0-0)
- [Xiangji Official Website](https://www.xiangjifanyi.com/)
- [Xiangji OpenAPI Documentation](https://openapi-doc.xiangjifanyi.com/)
- [Supported Languages](references/languages.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; helper scripts return JSON API responses and translated text or image URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Xiangji/Tosoiot API credentials, source language codes, target language codes, and text, local image files, or image URLs.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
