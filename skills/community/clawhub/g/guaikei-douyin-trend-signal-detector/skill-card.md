## Description:

Collects structured JSON from public Douyin keyword searches, creator posts, video comments, and real-time hot lists for content research, competitor analysis, sentiment review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content analysts, marketers, and research teams use this skill to gather public Douyin search results, creator posts, comments, and hot-list data for internal trend and competitor analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin keywords, profile or video URLs, and the GUAIKEI API token are sent to the provider service.

Mitigation: Use only approved queries, keep the token scoped and private, and rotate or revoke the token if it may have been exposed.

Risk: Fetched public data, including comments and user identifiers, can be retained locally in generated JSON logs.

Mitigation: Review, redact, or delete generated logs according to the team's data retention and privacy requirements.

Risk: The security evidence notes token transmission in URL query strings and promotional authentication-error output.

Mitigation: Treat the release as higher risk until the publisher moves token authentication out of query strings and removes promotional runtime messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-trend-signal-detector)
- [Guaikei token and access documentation](https://www.guaikei.com)
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

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON data on stdout with stderr logs and agent-facing command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; successful runs may save JSON logs under logs/.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
