## Description:

Fetches public Douyin keyword search results, creator posts, video comments, and trending feeds through CLI commands, returning structured JSON for analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content analysts use this skill to collect public Douyin search, creator, comment, and hot-list data for short-video content research, competitor monitoring, sentiment review, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin search terms, target URLs, limits, and GUAIKEI_API_TOKEN to www.guaikei.com.

Mitigation: Use only if that data transfer is acceptable, keep the token scoped to this service where possible, and rotate the token if it may have been exposed.

Risk: Fetched comments and account metadata can remain on disk in generated logs.

Mitigation: Review and delete generated logs after use, and avoid collecting or retaining data that should not be stored locally.

Risk: ClawHub security evidence marks the release suspicious because token handling is unsafe and runtime-disclosure claims conflict.

Mitigation: Review the release and security evidence before deployment, especially any workflows that expose environment variables, command output, or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-fetch-trending-feed)
- [Guaikei token and support site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Creator posts request schema](assets/post_cli_req.schema.json)
- [Creator posts response schema](assets/post_cli_resp.schema.json)
- [Comments request schema](assets/comment_cli_req.schema.json)
- [Comments response schema](assets/comment_cli_resp.schema.json)
- [Hot feed response schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI stdout returns structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 16.14.0 and GUAIKEI_API_TOKEN; command logs may be written under logs/.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md metadata, package.json, references/changelog.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
