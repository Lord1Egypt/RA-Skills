## Description:

Helps agents collect public Douyin data for content research, benchmark account analysis, comment sentiment insight, and trend tracking through keyword search, creator post retrieval, comment retrieval, and real-time hot list queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and marketing analysts use this skill to retrieve structured public Douyin content, creator, comment, and trend data for topic research, competitor monitoring, public opinion review, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin research queries and the Guaikei API token to guaikei.com during use.

Mitigation: Install only when this data sharing is acceptable, keep the token in a private environment, and rotate it if exposure is suspected.

Risk: Retrieved Douyin data is saved locally in generated JSON logs by default.

Mitigation: Treat generated logs as sensitive, avoid committing them to repositories, and delete or protect them after use.

## Reference(s):

- [Guaikei API website](https://www.guaikei.com)
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

**Output Type(s):** [Shell commands, API Calls, JSON, Files, Analysis, Guidance]

**Output Format:** [JSON results with concise Markdown guidance or analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes JSON logs locally by default and requires GUAIKEI_API_TOKEN for live API calls.]

## Skill Version(s):

1.0.0 (source: frontmatter metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
