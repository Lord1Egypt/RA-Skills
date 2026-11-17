## Description:

Collects public Douyin search results, creator posts, video comments, and hot topics through Node.js CLI commands, returning structured JSON for analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and marketing teams use this skill to gather public Douyin content, creator posts, comments, and hot topics for content research, competitor analysis, sentiment review, and trend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GUAIKEI_API_TOKEN handling may not fully match the skill's stated neutral-token behavior.

Mitigation: Use a narrowly scoped token, keep it in the environment only, review runtime output before deployment, and rotate the token if it is exposed.

Risk: The skill makes provider API calls and writes collected result data to local logs.

Mitigation: Run it only for clear public-data requests, limit collection to necessary fields, and handle generated logs as collected platform data.

Risk: Returned data or runtime behavior may include download-address fields despite the stated no-download scope.

Mitigation: Filter download URL fields from downstream use and avoid workflows that fetch, redistribute, or store media assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-scan-gather-output-posts)
- [Guaikei token and help site](https://www.guaikei.com)
- [Complete CLI options](references/options.md)
- [Changelog](references/changelog.md)
- [Search CLI request schema](assets/search_cli_req.schema.json)
- [Search CLI response schema](assets/search_cli_resp.schema.json)
- [Post CLI response schema](assets/post_cli_resp.schema.json)
- [Comment CLI response schema](assets/comment_cli_resp.schema.json)
- [Hot topics response schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands; executed CLI commands return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may write collected JSON results to local logs.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
