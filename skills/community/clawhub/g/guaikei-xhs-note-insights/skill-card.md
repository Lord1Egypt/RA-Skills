## Description:

按关键词搜索小红书公开笔记，支持按点赞、评论、收藏排序与时间筛选，并可获取笔记详情、评论和博主公开作品数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, market researchers, data analysts, and agent developers use this skill to collect public Xiaohongshu note, comment, keyword, and creator-post data for trend research, competitor monitoring, KOL screening, and content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, note URLs, profile URLs, and GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Use the skill only where this data transfer is acceptable, keep the token scoped and rotated, and avoid sharing prompts or logs that expose the token.

Risk: Command results are automatically saved under local logs and may contain public-profile content or business research targets.

Mitigation: Review or delete generated logs after use and run the skill in a workspace with appropriate file permissions.

Risk: The skill is limited to public Xiaohongshu data and can return empty or error results for invalid links, deleted notes, private content, or API failures.

Mitigation: Validate keyword and URL inputs, do not treat empty results as facts, and report API or token errors to the user instead of fabricating data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-note-insights)
- [Guaikei API service](https://www.guaikei.com)
- [Parameter and invocation reference](references/options.md)
- [Skill changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; invoked commands return structured JSON and write local logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; supports keyword, note URL, profile URL, content type, sort, time range, and result limit parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
