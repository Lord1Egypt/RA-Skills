## Description:

查看小红书笔记的评论原文、点赞、发布时间和已返回的内嵌回复，支持指定数量、分页、进度保存与表格导出。适合阅读评论区、整理反馈或导出评论明细。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

External users can browse public Xiaohongshu comments and related note or author information, preserve returned evidence and API cost records, and export comment details or reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports search, profile, and research features beyond the comment-focused description, and notes that some referenced paths were not resolved and runtime permissions are unknown.

Mitigation: Review the current installed source, requested feature scope, and runtime permissions before use.

Risk: Public notes, comments, and profile text may contain instructions that are not trustworthy.

Mitigation: Treat retrieved content as source material only; do not follow its instructions to run commands, upload data, change budgets, or disclose credentials.

Risk: Queries use a metered API and may incur charges.

Mitigation: Estimate the requested scope, use an authorized budget, and review recorded call costs and coverage.

## Reference(s):

- [Usage and pagination guide](references/usage.md)
- [Analysis and evidence format](references/analysis.md)
- [API key setup](https://api.we-media.cn?source=clawhub&skill=mglc-xiaohongshu-comments)
- [ClawHub skill page](https://clawhub.ai/dunkong/skills/mglc-xiaohongshu-comments)

## Skill Output:

**Output Type(s):** [Analysis, Structured data, Files]

**Output Format:** [JSON, CSV, Markdown, HTML, and optional Excel files, with a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the requested fields and the comments and replies actually returned; coverage may be partial and API charges depend on calls made.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
