## Description:

输入抖音视频链接后，该 skill 使用 HotBee 接口采集视频基础数据、转写文案、评论和封面/图集，并生成本地 HTML 拆解报告、评论 CSV/JSON、文案 Markdown 和报告卡片 SVG 等文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanye1402-hash](https://clawhub.ai/user/shanye1402-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, marketers, and agents use this skill to turn a user-provided public Douyin video link into a Chinese local report package for video breakdown, transcript extraction, comment insight, and reusable media/report assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provided Douyin links and derived media, comment, and transcript data are sent to HotBee and stored locally.

Mitigation: Use the skill only for user-provided public Douyin links, confirm the user is comfortable with HotBee processing, and keep generated output directories out of public repositories.

Risk: HotBee API key handling and custom API base URLs can expose credentials or send data to an unintended destination if misconfigured.

Mitigation: Use a dedicated HotBee key with limited quota, prefer the default API base, and use custom HOTBEE_API_BASE values only for HTTPS endpoints or controlled local testing.

## Reference(s):

- [HotBee 视频解析契约](artifact/references/hotbee-analysis-contract.md)
- [HotBee Skills](https://www.hotbee.cn/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown guidance plus local HTML, Markdown, CSV, JSON, SVG, image, and manifest files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include public Douyin author names, comments, transcript text, HotBee raw responses with sensitive fields redacted, warnings, and artifact paths.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
