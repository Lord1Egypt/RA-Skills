## Description:

翻译 JSON 文件中的指定文本字段，特别是 description 字段，并保持原始 JSON 结构完整。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeyeshield](https://clawhub.ai/user/jeyeshield)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, localization teams, and documentation maintainers use this skill to translate selected string fields in JSON files for product descriptions, API documentation, configuration text, datasets, and internationalization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected JSON field text is sent to MyMemory for translation and may expose sensitive or proprietary content to a third party.

Mitigation: Use the skill only with content approved for third-party translation services; avoid secrets, credentials, personal data, regulated data, proprietary configuration, and internal documents unless that transfer is approved.

Risk: Machine translation can be inaccurate or incomplete, especially for domain-specific text.

Mitigation: Review translated fields before using the output in production, customer-facing material, or regulated workflows.

## Reference(s):

- [MyMemory Translation API](https://api.mymemory.translated.net)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and generated UTF-8 JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Translated JSON preserves the original structure and marks failed translations while keeping the original text.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
