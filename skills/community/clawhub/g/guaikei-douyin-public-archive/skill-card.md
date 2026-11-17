## Description:

This skill helps agents search public Douyin content, collect creator posts and comments, and retrieve live hot lists for content planning, competitor analysis, sentiment review, and trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, and analysts use this skill to gather public Douyin search results, creator posts, comments, and hot-list data for short-video planning, competitive monitoring, public-opinion review, and trend tracking.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The security review flags credential and data-handling risk because Douyin queries, target URLs, and the GUAIKEI token are sent to the Guaikei service, and fetched public data may be saved locally as JSON logs.

Mitigation: Use only when that sharing and local storage are acceptable, protect and rotate the GUAIKEI token, and avoid sensitive research queries.

Risk: The security review labels the release suspicious due to review-worthy contradictions and runtime website or WeChat token prompts.

Mitigation: Review carefully before installing and treat token-acquisition prompts as vendor contact output rather than neutral security guidance.

## Reference(s):

- [Complete option reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search CLI request schema](assets/search_cli_req.schema.json)
- [Search CLI response schema](assets/search_cli_resp.schema.json)
- [Post CLI request schema](assets/post_cli_req.schema.json)
- [Post CLI response schema](assets/post_cli_resp.schema.json)
- [Comment CLI request schema](assets/comment_cli_req.schema.json)
- [Comment CLI response schema](assets/comment_cli_resp.schema.json)
- [Hot list CLI response schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands; CLI stdout and saved logs are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single command results are capped at 10,000 records and require a GUAIKEI_API_TOKEN.]

## Skill Version(s):

1.0.0 (source: evidence release, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
