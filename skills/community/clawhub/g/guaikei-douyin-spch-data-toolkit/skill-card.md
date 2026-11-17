## Description:

Queries public Douyin data for keyword search, hot lists, creator posts, and video comments, returning structured JSON for follow-on analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, marketers, and content operations teams use this skill to retrieve public Douyin search results, trending topics, creator posts, and comments for content planning, competitor monitoring, sentiment review, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin keywords, URLs, and the Guaikei API token to guaikei.com, including token-bearing request parameters.

Mitigation: Use only an approved, revocable token; confirm guaikei.com is acceptable for the intended data flow; rotate the token if logs, URLs, or errors expose it.

Risk: Fetched search, post, and comment datasets may be saved locally under the skill's logs directory.

Mitigation: Collect only the data needed for the task, delete logs that are no longer needed, and treat exported datasets as potentially sensitive operational records.

Risk: Returned media or download-style URLs are outside the stated skill boundary.

Mitigation: Use the skill for public-data retrieval and analysis only; review external media links before opening, sharing, or automating further processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-spch-data-toolkit)
- [Guaikei API access site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Creator posts request schema](assets/post_cli_req.schema.json)
- [Creator posts response schema](assets/post_cli_resp.schema.json)
- [Hot list response schema](assets/hot_cli_resp.schema.json)
- [Comment request schema](assets/comment_cli_req.schema.json)
- [Comment response schema](assets/comment_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON responses from Node.js CLI commands, with optional Markdown guidance from the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI logs are written to stderr, and fetched datasets may be saved under the skill's logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
