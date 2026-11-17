## Description:

Supports Douyin keyword search, creator post collection, video comment analysis, and real-time hot-list queries for content research, competitor analysis, public sentiment monitoring, trend tracking, viral-content discovery, and Douyin operations analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, content operations teams, and analysts use this skill to retrieve structured public Douyin search results, hot-list entries, creator posts, and comments through Node.js command-line tools. The returned JSON can support content planning, competitor monitoring, sentiment review, trend tracking, and follow-on reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GUAIKEI_API_TOKEN may have paid quota or broader access than needed.

Mitigation: Use a dedicated low-privilege token and review quota exposure before installing or running the commands.

Risk: Keywords, Douyin URLs, and fetched public data are sent to guaikei.com.

Mitigation: Confirm that external API use is permitted for the user's data-handling and authorization requirements before running searches or lookups.

Risk: Fetched search, post, and comment data is saved automatically under the skill logs directory.

Mitigation: Review retention needs and remove or protect logs that contain sensitive research targets, user handles, comments, or operational data.

Risk: The security verdict is suspicious because the API token is placed in URL query strings.

Mitigation: Avoid sharing command traces or logs that could expose request URLs, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-comments-extract)
- [Guaikei API token and support site](https://www.guaikei.com)
- [Complete option reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Post request schema](assets/post_cli_req.schema.json)
- [Post response schema](assets/post_cli_resp.schema.json)
- [Comment request schema](assets/comment_cli_req.schema.json)
- [Comment response schema](assets/comment_cli_resp.schema.json)
- [Hot-list response schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON command output with optional Markdown summaries and saved JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; commands write logs under the skill logs directory.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
