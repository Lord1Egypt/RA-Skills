## Description:

使用 GPT Image 2 基于一张或多张参考图生成新图片，在保留主体、布局或身份事实的同时改变风格、场景、材质、完成度和输出比例。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, designers, and developers use this skill to run GPT Image 2 image-to-image workflows from authorized reference images. It helps preserve specified identity, layout, structure, and product facts while changing style, scene, material, finish, or aspect ratio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote task metadata can cause downloaded result files to be written outside the chosen output folder.

Mitigation: Review before installing, use a dedicated output directory, avoid sensitive working directories, and fix filename sanitization before routine use.

Risk: The skill stores an AI Hive API key in a local configuration file when initialized.

Mitigation: Use only a trusted AI Hive account and store the API key locally only when comfortable with a config file at ~/.ai-hive/config.json.

Risk: Reference images may include sensitive, unauthorized, or commercially restricted content.

Mitigation: Use only authorized reference images and retain the original image, prompt, task ID, and approval record for review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/gpt-image-2-image-to-image)
- [AI Hive API endpoint used by the skill](https://ai-hive.iclip.cn/api)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an AI Hive API key, uploads explicit reference images, submits fixed GPT Image 2 image-generation tasks, and can write generated result files to a selected output directory.]

## Skill Version(s):

1.0.1 (source: server release evidence and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
