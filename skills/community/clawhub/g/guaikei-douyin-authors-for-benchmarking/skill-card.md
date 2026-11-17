## Description:

Retrieves public Douyin search results, hot-list entries, author posts, and comments for short-video research, competitor analysis, trend tracking, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and analysts use this skill to collect structured public Douyin data for keyword research, hot-list monitoring, author-post collection, comment analysis, competitor benchmarking, and content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin queries, URLs or IDs, and the GUAIKEI_API_TOKEN to Guaikei.

Mitigation: Use only approved tokens and inputs that are acceptable to share with Guaikei before running the CLI.

Risk: Fetched results are saved locally as JSON logs and may include comments, creator identifiers, URLs, or sensitive research topics.

Mitigation: Run the skill in an appropriate workspace, review retained logs, and delete or protect them when the analysis is complete.

Risk: The skill is limited to public Douyin data and should not be used for private, hidden, or login-only content.

Mitigation: Confirm the request targets public data and stop or clarify when a user asks for non-public or login-state data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-authors-for-benchmarking)
- [Guaikei API Website](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search Request Schema](assets/search_cli_req.schema.json)
- [Search Response Schema](assets/search_cli_resp.schema.json)
- [Post Request Schema](assets/post_cli_req.schema.json)
- [Post Response Schema](assets/post_cli_resp.schema.json)
- [Comment Request Schema](assets/comment_cli_req.schema.json)
- [Comment Response Schema](assets/comment_cli_resp.schema.json)
- [Hot List Response Schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [json, shell commands, guidance]

**Output Format:** [Structured JSON from CLI stdout, with operational logs on stderr and optional Markdown guidance around command use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; fetched results may be saved as local JSON logs.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
