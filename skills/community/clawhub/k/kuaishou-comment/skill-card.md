## Description:

快手评论分析工具。输入作品链接即可获取一级评论数据，支持分页浏览、评论情感分析（积极/负面/需求/竞品），生成 HTML 报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operations teams, data analysts, brands, and MCNs use this skill to fetch Kuaishou comment pages, review comment tables, analyze sentiment across positive, negative, demand, and competitor categories, and export local HTML reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requested Kuaishou opus IDs to RedFox and requires a RedFox API key.

Mitigation: Verify the key source, scope, lifetime, and revocation path before use; keep REDFOX_API_KEY in environment or agent configuration rather than prompts, logs, code, or output files.

Risk: Generated HTML reports contain comment data and may load avatar URLs from comment sources.

Mitigation: Open generated reports only when the comment source is trusted, or sanitize external avatar URLs and report content before viewing or sharing.

Risk: Documented usage passes JSON through shell command arguments, which can be fragile for large or untrusted content.

Mitigation: Prefer stdin or file-based JSON transfer for analysis and page data when running the helper scripts.

Risk: The consolidated report script opens generated HTML automatically.

Mitigation: Make browser opening an explicit user choice or review the output path before opening the file.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/redfox-data/redfox-community/tree/main/skills/kuaishou-comment)
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/kuaishou-comment)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=github)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML files, shell commands, guidance]

**Output Format:** [Markdown responses with comment tables and sentiment summaries, JSON from helper scripts, and generated local HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; sends requested Kuaishou opus IDs to RedFox; generated reports may include comment data, avatar URLs, and AI-written summaries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
