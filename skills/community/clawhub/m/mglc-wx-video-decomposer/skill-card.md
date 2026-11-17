## Description:

基于曼格云 API 拆解视频号分享链接或本地视频，生成带有时间点证据的内容分析与改稿建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者和运营人员用它拆解视频号作品的画面、脚本及互动数据，形成有证据的优化建议和可导出的报告。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected video and metadata are sent to an external analysis service and temporary upload storage.

Mitigation: Obtain consent before upload and paid calls; use only media you are permitted to share.

Risk: An exposed API key can enable unauthorized access or charges.

Mitigation: Keep WM_API_KEY in a local environment variable or config file, not in chat or exported reports.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dunkong/skills/mglc-wx-video-decomposer)
- [API documentation](artifact/references/api.md)
- [Analysis schema](artifact/references/analysis-schema.md)
- [曼格云 AI 接入指南](https://api.we-media.cn/client/ai-guide)
- [曼格云产品文档](https://api.we-media.cn/client/products)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Files]

**Output Format:** [Text guidance and local Markdown, Excel (.xlsx), HTML and JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include timestamped evidence, interaction facts and actual API consumption.]

## Skill Version(s):

1.4.0 (source: skill metadata and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
