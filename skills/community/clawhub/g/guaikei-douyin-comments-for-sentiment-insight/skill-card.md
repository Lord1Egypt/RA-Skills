## Description:

Retrieves public Douyin search results, creator posts, video comments, and trending topics as structured JSON for content research, competitor analysis, sentiment insight, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect public Douyin data for short-video topic research, competitor account monitoring, comment sentiment review, and trend tracking. It is not intended for publishing videos, downloading watermarked content, private backend data, or non-Douyin platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin keywords, target URLs, and GUAIKEI_API_TOKEN to the provider service.

Mitigation: Install only when that data sharing is acceptable, keep the token secret, and avoid broad automatic invocation.

Risk: Fetched results are saved locally by default and may include collected comment or creator data.

Mitigation: Review the logs directory after use and clear retained results when they are no longer needed.

Risk: Large-scale comment or creator collection can create compliance and data-handling concerns.

Mitigation: Limit collection to open content and use the results only within the approved personal or team workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-comments-for-sentiment-insight)
- [Repository listed in metadata](https://github.com/um-why/douyin-search-openclaw)
- [Guaikei token service](https://www.guaikei.com)
- [Complete options](references/options.md)
- [Changelog](references/changelog.md)
- [Search CLI request schema](assets/search_cli_req.schema.json)
- [Search CLI response schema](assets/search_cli_resp.schema.json)
- [Post CLI request schema](assets/post_cli_req.schema.json)
- [Post CLI response schema](assets/post_cli_resp.schema.json)
- [Comment CLI request schema](assets/comment_cli_req.schema.json)
- [Comment CLI response schema](assets/comment_cli_resp.schema.json)
- [Hot CLI response schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON on stdout with stderr logs and saved JSON log files by default]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; supports search, creator posts, comments, and hot-list commands with documented limits up to 10000 records per call.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
