## Description:

使用 Nano Banana Pro 把美图 Meitu、美图秀秀、美图设计室、WHEE 或美图云修中的图片生成与编辑需求迁移为可复现的 AI Hive 工作流，覆盖商品精修、自然人像调整、海报背景、批量 SKU 和社媒适配。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, and developers use this skill to convert Meitu-style image generation and editing tasks into repeatable AI Hive workflows for products, portraits, posters, SKU batches, and social media crops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads user-selected reference images and downloads generated outputs through AI Hive and server-provided storage URLs.

Mitigation: Avoid private or regulated source images unless the deployment has reviewed the AI Hive data path, URL validation, host constraints, and retention expectations.

Risk: The security evidence reports that upload and download URLs are trusted from the service response and that host constraints and size limits should be clearer.

Mitigation: Run the skill in a controlled environment, pin dependencies, and add or verify URL allowlists and file-size limits before production use.

Risk: Generated edits may alter identity, labels, product details, claims, or text in commercially sensitive images.

Mitigation: Review each output against the source assets and place critical Chinese text, prices, and legal statements in a separate post-production step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/meitu-image-generation-editing-alternative)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and a Python CLI script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can submit AI Hive image generation tasks, upload selected reference images, poll task status, and download generated image files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
