## Description:

按小红书作者主页或作者 ID 整理公开作品列表，支持分页、数量上限、恢复进度以及 Excel、JSON 导出。适合盘点博主笔记、整理作品清单和查近期更新。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

适合需要盘点小红书作者公开作品、整理近期更新并按需导出作品清单的用户。可将返回数据用于带出处的摘要与分析；列表不代表完整历史，也不等于逐篇读取正文。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes that the bundled skill supports broader Xiaohongshu research, including search and comment collection, than the author-post listing purpose suggests; scan coverage is incomplete.

Mitigation: Before installing, review the skill's permissions and decide whether those broader research features are needed.

Risk: API queries can incur customer-price charges.

Mitigation: Estimate the requested scope and use an explicitly authorized budget before running a query.

## Reference(s):

- [使用说明（参数、分页与费用）](references/usage.md)
- [分析与证据格式](references/analysis.md)
- [曼格云 API 服务](https://api.we-media.cn)

## Skill Output:

**Output Type(s):** [JSON, CSV, Markdown, HTML, Excel spreadsheet, Evidence-based analysis]

**Output Format:** [公开作品数据、引用证据和报告文件；可导出 JSON、CSV、Markdown、HTML 及可选 XLSX。]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [结果覆盖本次接口实际返回的数据；列表不保证完整历史。接口调用按客户价格计费。]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
