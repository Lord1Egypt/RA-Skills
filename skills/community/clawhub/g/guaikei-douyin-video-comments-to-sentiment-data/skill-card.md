## Description:

当用户需要公开数据支撑抖音相关决策时，使用本技能：关键词搜索排序、博主作品批量抓取、评论抓取分析、实时热榜查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to collect public Douyin keyword-search results, author posts, video comments, and trending topics for marketing selection, content planning, trend research, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends keywords, Douyin URLs, and fetched public results to www.guaikei.com.

Mitigation: Use it only for public Douyin research, avoid sensitive research terms, and confirm that this data sharing is acceptable before running commands.

Risk: The security review reports unsafe API token handling.

Mitigation: Use a limited token where possible, keep GUAIKEI_API_TOKEN out of shared logs or shell history, and rotate the token if exposure is suspected.

Risk: Authentication failures may show vendor contact information despite the skill claiming neutral runtime errors.

Mitigation: Review auth-error output before deployment and avoid exposing raw stderr directly to end users.

Risk: Successful search, post, and comment results are saved locally under logs.

Mitigation: Review, protect, and delete generated log files according to the user's data-retention needs.

## Reference(s):

- [Complete CLI options](references/options.md)
- [Changelog](references/changelog.md)
- [Request and response JSON Schemas](assets/)

## Skill Output:

**Output Type(s):** [shell commands, JSON, files, guidance]

**Output Format:** [Markdown guidance with bash commands; CLI stdout returns JSON and successful search, post, and comment runs save JSON logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and Node.js >= 16.14.0.]

## Skill Version(s):

1.0.0 (source: SKILL.md metadata, package.json, references/changelog.md, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
