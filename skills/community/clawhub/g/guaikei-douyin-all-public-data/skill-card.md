## Description:

Provides structured JSON access to public Douyin keyword search, creator posts, video comments, and real-time trending lists for content research, competitor analysis, sentiment review, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and analysts use this skill to collect public Douyin search results, creator posts, comments, and trending topics for marketing research, content planning, competitor monitoring, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin keywords, profile or video URLs, and GUAIKEI_API_TOKEN to www.guaikei.com.

Mitigation: Use it only when that data sharing is acceptable, treat GUAIKEI_API_TOKEN as sensitive, and rotate or monitor the token if needed.

Risk: Local logs may contain research topics, URLs, and collected public comments.

Mitigation: Review log retention and delete or disable logs when topics or collected comments are sensitive.

Risk: Ambiguous user requests could trigger Douyin data collection the user did not intend.

Mitigation: Confirm ambiguous requests before invoking search, creator post, comment, or hot-list commands.

Risk: Server security evidence reports credential-handling and disclosure problems.

Mitigation: Review the security guidance before installation and avoid exposing token, support, or contact details in runtime outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-all-public-data)
- [Guaikei token and usage site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Post request schema](assets/post_cli_req.schema.json)
- [Post response schema](assets/post_cli_resp.schema.json)
- [Comment request schema](assets/comment_cli_req.schema.json)
- [Comment response schema](assets/comment_cli_resp.schema.json)
- [Hot list response schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [JSON to stdout with optional JSON log files and Markdown shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and sends requests to www.guaikei.com; command results follow the bundled JSON schemas.]

## Skill Version(s):

1.0.0 (source: package.json, changelog, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
