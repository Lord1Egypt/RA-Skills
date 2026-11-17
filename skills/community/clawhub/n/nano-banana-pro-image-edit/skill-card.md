## Description:

使用 Nano Banana Pro 按自然语言编辑现有图片，同时明确保留区、修改区和禁止变化项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, ecommerce operators, and developers use this skill to edit existing images with explicit preserve, change, allowed-adjustment, prohibited-change, and acceptance criteria before calling AI Hive image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses an AI Hive API key and can send it to a configurable API server.

Mitigation: Use only the default official AI Hive base URL, avoid untrusted --base-url or AI_HIVE_BASE_URL values, and keep the configuration file restricted to the current user.

Risk: Images provided with --image are uploaded to the AI Hive service for processing.

Mitigation: Review images before upload, avoid unnecessary sensitive content, and run the tool from an isolated Python environment when evaluating the release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-pro-image-edit)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and natural-language image-editing prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces prompts and commands for uploading source images, submitting Nano Banana Pro image edits, polling tasks, and downloading image files.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
