## Description:

把小红书关键词搜索、笔记详情、笔记评论、博主作品抓取为结构化数据，一次最多 1W 条；用于获取公开小红书内容数据以便后续汇总、对比或报告，不用于发布、互动或私密内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, marketers, data analysts, and agent developers use this skill to retrieve public Xiaohongshu keyword results, note details, comments, and creator post lists for later analysis, comparison, KOL screening, trend review, or reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, URLs, limits, and GUAIKEI_API_TOKEN to Guaikei for processing.

Mitigation: Install and run it only when that processing is acceptable; protect the token, avoid sharing it in prompts or logs, and rotate it if exposed.

Risk: Generated logs may contain public comments, profile data, request details, and xsec_token-bearing links.

Mitigation: Review, restrict access to, or delete generated log files after use according to the data handling needs of the task.

Risk: The skill is intended for public or authorized Xiaohongshu data and does not support private, hidden, login-gated, publishing, or interaction workflows.

Mitigation: Use it only for authorized public-data retrieval and stop rather than attempting to bypass platform access boundaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-kol-evaluation-data)
- [Guaikei API and token service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands; executed commands return structured JSON on stdout and may save JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; supports keyword, URL, content type, sort, time, and limit parameters with a maximum request limit of 10000.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
