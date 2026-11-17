## Description:

商品短视频广告。卖点 → 分镜脚本 → 分段生成 → 拼接加字幕成片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

电商卖家和营销人员可用此技能把商品卖点转成多镜头短视频广告脚本，逐镜生成片段，并制作带字幕的成片。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference images may be sent to external model providers; the security review reports unclear disclosure and partial inspection of some components.

Mitigation: Before use, check which provider and inputs are involved and decide whether you are comfortable sending them; treat behavior in partially inspected components as unverified.

## Reference(s):

- [ClawHub release](https://clawhub.ai/dlazyai/skills/product-video-ad)
- [Provider CLI guide](references/provider-cli.md)
- [Video backend guide](references/video-backends.md)
- [Related skill: main-image-video](https://github.com/dlazy-ai/ecommerce-skills/blob/main/skills/main-image-video/skill.md)
- [Related skill: ugc-testimonial](https://github.com/dlazy-ai/ecommerce-skills/blob/main/skills/ugc-testimonial/skill.md)
- [dLazy CLI source](https://github.com/dlazy-ai/cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Storyboard prompts and captions, JSON shot boards, SRT subtitles, and generated MP4 video clips and ads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shot durations and captions follow the storyboard; audio narration and music are not produced by this skill.]

## Skill Version(s):

1.0.30 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
