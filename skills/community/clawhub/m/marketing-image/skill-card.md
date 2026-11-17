## Description:

使用 Nano Banana 2 建立可跨渠道派生的营销图片系统：先做 Campaign 母版，再生成发布会、活动、线索收集、节日促销和社媒尺寸变体。Use this skill for 营销图片、营销视觉、Campaign KV、活动主视觉、推广图、促销图、发布会海报、EDM、官网 Hero、社媒广告、小红书抖音微信 Instagram LinkedIn 内容；通过 AI Hive 生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, designers, and developers use this skill to generate campaign master visuals and channel-specific marketing image variants through AI Hive. It supports product launches, event signup graphics, B2B lead collection visuals, holiday promotion drafts, and social or web size adaptations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference image uploads may send disguised or symlinked local files to AI Hive.

Mitigation: Use only known real image files from trusted locations, avoid symlinked paths, and review local file arguments before running generation or upload commands.

Risk: Prompts and reference images are transmitted to an external AI Hive service.

Mitigation: Do not include private, confidential, or unapproved campaign material unless the user has approved sending it to AI Hive.

Risk: Unpinned Python dependencies may change behavior over time.

Mitigation: Install dependencies in an isolated environment and pin reviewed versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/marketing-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with bash commands; the script submits image-generation jobs, prints task JSON or status text, and downloads generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed Nano Banana 2 public model through AI Hive, accepts optional local reference images, supports batch size and model parameters, and can save outputs to a local directory.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
