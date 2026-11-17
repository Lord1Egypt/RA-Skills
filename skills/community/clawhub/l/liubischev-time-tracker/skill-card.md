## Description:

基于柳比歇夫方法的时间与精力管理助理，通过飞书多维表格存储数据，支持自然语言记录与日报生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ylstf](https://clawhub.ai/user/ylstf)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to convert natural-language activity notes into structured time records and Feishu-backed daily reports. It supports personal time and energy tracking, parallel activity summaries, tag reuse, and brief energy insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal Feishu activity data may be read or persisted too broadly when multiple people share one base.

Mitigation: Use a dedicated Feishu account or isolated base with least-privilege access for each deployment.

Risk: Setup and script logs can expose Feishu base tokens, table IDs, or other sensitive identifiers.

Mitigation: Avoid sharing logs, redact base identifiers before support review, and store generated IDs in a private configuration channel.

Risk: The skill depends on lark-cli for authenticated Feishu operations.

Mitigation: Pin and verify lark-cli before authentication, and prefer dry-run or explicit confirmation before scheduled or manual daily report writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ylstf/skills/liubischev-time-tracker)
- [Publisher profile](https://clawhub.ai/user/ylstf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON records, Markdown daily reports, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily reports may be written to Feishu unless dry-run mode is used.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
