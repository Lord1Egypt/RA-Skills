## Description:

Retrieves public Douyin search results, creator posts, video comments, and real-time hot-list data through command-line calls for content analysis, competitor monitoring, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External developers, analysts, and marketing or content teams use this skill to turn natural-language Douyin data requests into keyword searches, creator post collection, comment retrieval, and hot-topic checks for internal analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin URLs, keywords, limits, and GUAIKEI_API_TOKEN are sent to the Guaikei API.

Mitigation: Confirm the user wants Douyin data before execution, use the least-privileged token available, and rotate or revoke tokens when access changes.

Risk: Retrieved public data is automatically saved to local logs.

Mitigation: Clear generated logs on shared machines and avoid retaining collected data longer than needed for the analysis.

Risk: Broad natural-language triggers can activate the skill for ambiguous prompts.

Mitigation: Ask for confirmation when the requested platform, data type, or collection intent is unclear.

Risk: Runtime messages may contradict documented token-handling claims.

Mitigation: Review authentication failure behavior before deployment and avoid exposing operational contact or marketing text to end users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-data-feed)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search CLI Request Schema](assets/search_cli_req.schema.json)
- [Search CLI Response Schema](assets/search_cli_resp.schema.json)
- [Post CLI Request Schema](assets/post_cli_req.schema.json)
- [Post CLI Response Schema](assets/post_cli_resp.schema.json)
- [Comment CLI Request Schema](assets/comment_cli_req.schema.json)
- [Comment CLI Response Schema](assets/comment_cli_resp.schema.json)
- [Hot CLI Response Schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON on stdout with operational logs on stderr and local JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and GUAIKEI_API_TOKEN; supports search, creator posts, comments, and hot-list commands with documented limits.]

## Skill Version(s):

1.0.0 (source: package.json, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
