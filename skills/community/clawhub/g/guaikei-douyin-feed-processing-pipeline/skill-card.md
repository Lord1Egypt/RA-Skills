## Description:

Retrieves public Douyin search results, creator posts, video comments, and hot-list data through four Node.js command-line tools that return JSON for downstream analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams use this skill to collect structured public Douyin data for content research, competitor monitoring, comment analysis, trend tracking, and marketing reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token and requested Douyin keywords, URLs, and IDs may be sent to Guaikei during execution.

Mitigation: Use the skill only for approved public-data research, avoid sensitive searches on shared systems, and rotate GUAIKEI_API_TOKEN if exposure is suspected.

Risk: Fetched results are automatically saved as local JSON logs.

Mitigation: Protect, review, or delete generated log files after use, especially on shared or synced machines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-feed-processing-pipeline)
- [Guaikei Douyin data service](https://www.guaikei.com)
- [Complete options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Creator posts request schema](assets/post_cli_req.schema.json)
- [Creator posts response schema](assets/post_cli_resp.schema.json)
- [Hot-list response schema](assets/hot_cli_resp.schema.json)
- [Comment request schema](assets/comment_cli_req.schema.json)
- [Comment response schema](assets/comment_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Guidance]

**Output Format:** [JSON on stdout with operational logs on stderr and optional saved JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; exits with code 0 for success or empty results, 1 for runtime errors, and 3 for missing or invalid token.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill frontmatter, package.json, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
