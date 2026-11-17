## Description:

Retrieves public Douyin search results, creator posts, video comments, and hot-list data for content research, competitor monitoring, opinion analysis, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External operators, marketers, and analysts use this skill to collect structured public Douyin data for short-video topic research, competitor account review, comment analysis, and trend monitoring. It does not perform posting, liking, commenting, following, login-based access, or marketing strategy decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin keywords, target URLs or IDs, and a reusable Guaikei API token to guaikei.com.

Mitigation: Install and run it only when that data sharing is acceptable; prefer an API design that sends the token in an authorization header with explicit permission scope.

Risk: Fetched Douyin result data is saved locally by default.

Mitigation: Avoid sensitive competitor or personal-data research on shared machines, and manage or delete generated log files after use.

Risk: Ambiguous trigger wording can cause the skill to run for broad competitor-analysis requests before the target platform or input is clear.

Mitigation: Ask for a Douyin keyword, video link, creator profile, or hot-list intent before executing a command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-comment-threads)
- [Guaikei API site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Post request schema](assets/post_cli_req.schema.json)
- [Post response schema](assets/post_cli_resp.schema.json)
- [Hot-list response schema](assets/hot_cli_resp.schema.json)
- [Comment request schema](assets/comment_cli_req.schema.json)
- [Comment response schema](assets/comment_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Files, Guidance]

**Output Format:** [JSON responses on stdout, operational logs on stderr, and JSON result files under logs/]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; supported commands cover search, creator posts, comments, and hot-list retrieval.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json, SKILL.md metadata, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
