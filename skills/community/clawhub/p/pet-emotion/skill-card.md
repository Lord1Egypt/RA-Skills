## Description:

上传猫或狗的照片后，技能使用 DashScope 多模态模型识别快乐、悲伤、愤怒、恐惧、放松或警觉情绪，并生成带置信度、解读和可视化图表的 HTML 报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect a cat or dog photo, summarize a likely momentary emotion, and produce a shareable HTML report with confidence, reasoning, and interaction suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling can use an unrelated OPENAI_API_KEY if DASHSCOPE_API_KEY is absent.

Mitigation: Use a dedicated DashScope key, prefer DASHSCOPE_API_KEY, and avoid running the skill in environments that contain unrelated API keys.

Risk: Pet photos are sent to DashScope for analysis.

Mitigation: Analyze only photos the user is comfortable uploading to that third-party service and avoid sensitive images.

Risk: Generated HTML reports are considered untrusted until the template escaping issue is fixed.

Mitigation: Review or sanitize report content before opening or sharing generated HTML, and run the skill in a constrained environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/pet-emotion)
- [Project homepage](https://github.com/bettermen/pet-emotion)
- [宠物情绪解读知识库](references/emotion_guide.md)
- [DashScope API key console](https://dashscope.console.aliyun.com/apiKey)
- [DashScope compatible chat completions endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown summary, shell commands, configuration guidance, and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local pet image and a DashScope API key; image data is uploaded to the configured model endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
