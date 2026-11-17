## Description:

使用 Nano Banana Pro 制作自然、连续、平台原生的生活方式种草图片，让同一人物、商品、空间与时间线形成可信内容系列。Use this skill for Nano Banana Pro seeding content、小红书笔记、好物分享、生活方式图文、Instagram carousel、抖音图文、穿搭、美妆、家居、旅行和UGC风格素材；通过 AI Hive 生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and ecommerce teams use this skill to guide agents in producing coherent lifestyle seeding image series for social and commerce channels. It emphasizes continuity across people, products, spaces, timelines, and disclosure requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic result downloads can write server-controlled files outside the chosen output folder.

Mitigation: Use --no-download or run with an isolated output directory until filename containment and download size limits are fixed.

Risk: Custom API endpoints can change the trust boundary for prompts, media, API keys, and returned files.

Mitigation: Use the official AI Hive endpoint or another endpoint you fully trust; avoid custom --base-url values.

Risk: Initialization stores an API key in the user's home directory.

Mitigation: Review local credential storage, keep dependencies in a virtual environment, and rotate any exposed API key.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/nano-banana-pro-seeding-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and generated image task output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI Hive credentials and can upload reference media, poll generation tasks, and download generated image files unless no-download mode is used.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
