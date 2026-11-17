## Description:

提示词美学用楚歌AIGC美学框架，将一句图像需求生成可用于 GPT-image2 的中英双语高完成度提示词，并内置 32 种风格模板、五角色色彩分配和负面清单质检。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chugenice](https://clawhub.ai/user/chugenice)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative teams use this skill to turn a short image concept into a structured GPT-image2 prompt. It selects an aesthetic template, fills scene and typography parameters, applies color-role guidance, and returns Chinese and English prompt text with brief usage guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad routing may capture general image-prompt requests intended for another model or medium.

Mitigation: Apply the documented boundary: use this skill only for GPT-image2 image-generation requests, not Midjourney, DALL-E, video, 3D, UI, or pure text tasks.

Risk: Generated bilingual prompts may include user-supplied visible text, brand copy, or aesthetic choices that need review before image generation.

Mitigation: Review the Chinese prompt, English prompt, and usage note before submitting to GPT-image2; adjust text, aspect ratio, and constraints as needed.

## Reference(s):

- [Template Library](artifact/references/templates.md)
- [ClawHub Skill Page](https://clawhub.ai/chugenice/skills/prompt-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with Chinese and English prompt sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a selected style label, a filled Chinese prompt, an English prompt, and brief GPT-image2 usage guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
