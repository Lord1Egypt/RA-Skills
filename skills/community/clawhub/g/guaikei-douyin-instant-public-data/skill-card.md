## Description:

Fetches public Douyin search results, creator posts, video comments, and hot-list data through Guaikei CLI commands for content research and trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, marketers, and content teams use this skill to collect structured public Douyin data for content ideation, competitor monitoring, comment analysis, and hot-topic tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad auto-activation may run the skill for ambiguous short-video research requests even when the user did not explicitly request Douyin.

Mitigation: Confirm the target platform and task before invoking the CLI when the request is ambiguous.

Risk: Search terms, creator URLs, video URLs, and a GUAIKEI API token are sent to a third-party service.

Mitigation: Use only non-sensitive public-data queries, keep the token in the environment, and avoid sharing private or confidential URLs or keywords.

Risk: Runs may create local JSON logs containing query parameters and collected public data.

Mitigation: Review, protect, rotate, or delete generated logs according to the user's data-handling policy.

Risk: Security evidence reports review-worthy token-handling and runtime-message concerns.

Mitigation: Review before installation and prefer a revised release that uses an Authorization header, narrows activation, and removes runtime promotional or contact messages.

## Reference(s):

- [Skill README](readme.md)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search CLI Request Schema](assets/search_cli_req.schema.json)
- [Search CLI Response Schema](assets/search_cli_resp.schema.json)
- [Post CLI Request Schema](assets/post_cli_req.schema.json)
- [Post CLI Response Schema](assets/post_cli_resp.schema.json)
- [Comment CLI Request Schema](assets/comment_cli_req.schema.json)
- [Comment CLI Response Schema](assets/comment_cli_resp.schema.json)
- [Hot CLI Response Schema](assets/hot_cli_resp.schema.json)
- [Guaikei Token and Help Site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, json, guidance]

**Output Format:** [JSON from CLI stdout with logs and status messages on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and a GUAIKEI_API_TOKEN environment variable; successful CLI runs may also save JSON logs under logs/.]

## Skill Version(s):

1.0.0 (source: package.json, references/changelog.md, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
