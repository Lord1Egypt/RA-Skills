## Description:

Poster Maker guides agents through style replication, creative product poster generation, and livestream teaser poster workflows, with prompt templates and an optional image-generation script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dizhu](https://clawhub.ai/user/dizhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, designers, and agents use this skill to plan, prompt, generate, and iterate ecommerce, campaign, social media, brand, and livestream posters. It helps collect product details, approved copy, composition choices, and prompt constraints before optional image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can send an OpenRouter API key to the Ofox image-generation endpoint.

Mitigation: Use a dedicated Ofox key with spending limits, do not use an OpenRouter key with this version, and rotate any OpenRouter key previously used with the script.

Risk: Prompts and poster content are sent to an external image-generation API when the helper script runs.

Mitigation: Avoid sensitive prompt content and review the script before installing or executing it.

## Reference(s):

- [Prompt Templates](references/Prompt模板.md)
- [Copywriting Principles](references/文案原则.md)
- [Style Analysis Guide](references/风格分析指南.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown guidance with prompt templates and optional shell commands; the helper script can write PNG image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses external image-generation APIs when the optional script is run and requires API-key configuration.]

## Skill Version(s):

1.7.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
