## Description:

漫剧美术总监帮助代理生成统一画风、角色资产、场景资产和逐镜头 AI 绘图 Prompt，用于保持漫剧分镜的角色与视觉一致性。

This skill is ready for commercial/non-commercial use.

## Publisher:

[samwang-001](https://clawhub.ai/user/samwang-001)

### License/Terms of Use:

MIT-0

## Use Case:

Comic creators, writers, and agent workflows use this skill to turn storyboard or frame requirements into consistent character assets, scene descriptions, and image-generation prompts. It is intended for Chinese-language comic art direction across Midjourney, Stable Diffusion, 即梦AI, and 可灵 workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger terms such as art, character design, and scene design may activate the skill more often than intended.

Mitigation: Use explicit activation or workflow routing when the task requires comic art prompt generation.

Risk: Tool-specific prompt conventions may not match every image-generation model or product version.

Mitigation: Review and adjust the generated prompts and parameters for the target image tool before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samwang-001/skills/manju-artist)
- [Server-resolved GitHub provenance](https://github.com/samwang-001/manju-skills/tree/main/manju-artist)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style Chinese prompt package with style terms, character assets, scene descriptions, positive prompts, negative prompts, and tool parameters.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses 9:16 vertical-frame conventions and includes tool-specific guidance for Midjourney, Stable Diffusion, 即梦AI, and 可灵.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
