## Description:

Collects public Douyin search results, creator posts, video comments, and real-time hot rankings through Node.js CLI commands that return structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users and content analysts use this skill to collect public Douyin data for short-video topic research, competitor monitoring, sentiment review, and trend tracking. Developers can call the included CLI commands from an agent workflow and consume the returned JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad public-data collection can gather more Douyin account, comment, or trend data than a user intended.

Mitigation: Require a specific task and keep limits no higher than needed for the analysis.

Risk: Queries and results may be saved as local JSON logs.

Mitigation: Treat logs as sensitive work product and delete or restrict them after use.

Risk: The GUAIKEI_API_TOKEN may be included in service request parameters.

Mitigation: Use a limited, revocable token and avoid running the skill where request URLs are broadly logged.

Risk: Collected public-platform data may be subject to platform terms or privacy obligations.

Mitigation: Verify the planned collection and downstream use against applicable rules before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-public-content-to-dataset-export)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei token and support site](https://www.guaikei.com)
- [Complete CLI options](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Post request schema](assets/post_cli_req.schema.json)
- [Post response schema](assets/post_cli_resp.schema.json)
- [Comment request schema](assets/comment_cli_req.schema.json)
- [Comment response schema](assets/comment_cli_resp.schema.json)
- [Hot ranking response schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration guidance]

**Output Format:** [JSON on stdout, diagnostics on stderr, and saved JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14.0 and GUAIKEI_API_TOKEN; commands accept bounded keyword, URL, limit, sort, time, duration, and content parameters.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
