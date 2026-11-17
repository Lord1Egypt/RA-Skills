## Description:

Retrieves structured public Douyin search results, creator posts, video comments, and real-time hot-list data for content research, competitor monitoring, sentiment analysis, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, marketers, analysts, and agent developers use this skill to retrieve public Douyin data for topic research, competitor monitoring, comment analysis, hot-list tracking, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin query and link inputs, together with GUAIKEI_API_TOKEN, are sent to guaikei.com.

Mitigation: Install only when that data transfer is acceptable; use a limited-quota token and rotate it if exposed.

Risk: Generated logs may contain stored social-media datasets, including personal information from public Douyin content.

Mitigation: Keep logs private, restrict access to exports, and delete datasets that are no longer needed.

Risk: The security evidence verdict is suspicious because of token handling and automatic local storage of bulk results.

Mitigation: Review the skill before deployment and confirm token, quota, and data-handling requirements with the owning team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-authors-scrape)
- [Guaikei API site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search CLI request schema](assets/search_cli_req.schema.json)
- [Search CLI response schema](assets/search_cli_resp.schema.json)
- [Post CLI request schema](assets/post_cli_req.schema.json)
- [Post CLI response schema](assets/post_cli_resp.schema.json)
- [Hot-list CLI response schema](assets/hot_cli_resp.schema.json)
- [Comment CLI request schema](assets/comment_cli_req.schema.json)
- [Comment CLI response schema](assets/comment_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Command-line JSON on stdout with logs on stderr; agent guidance may be Markdown text with inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; successful runs may save retrieved Douyin datasets under logs/.]

## Skill Version(s):

1.0.0 (source: server release, frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
