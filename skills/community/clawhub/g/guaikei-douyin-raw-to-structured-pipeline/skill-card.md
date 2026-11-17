## Description:

Retrieves structured public Douyin data for keyword search, creator posts, video comments, and real-time trending topics with filtering and JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External developers, analysts, and content or marketing teams use this skill to fetch public Douyin search results, creator posts, comments, and trending-topic data for content research, competitor monitoring, public-opinion analysis, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Guaikei API tokens may be paid, shared, or otherwise high-value.

Mitigation: Use a restricted token where possible, keep the skill in a private workspace, avoid exposing the token in shared logs or transcripts, and rotate the token if exposure is suspected.

Risk: Keywords and Douyin URLs or IDs are sent to Guaikei during data retrieval.

Mitigation: Confirm that the searched topics and target URLs are appropriate for third-party processing before running the commands.

Risk: Retrieved datasets may be saved locally and can contain sensitive monitoring context.

Mitigation: Review and clean the local logs directory after use, especially in shared workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-raw-to-structured-pipeline)
- [Guaikei API website](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Creator posts request schema](assets/post_cli_req.schema.json)
- [Creator posts response schema](assets/post_cli_resp.schema.json)
- [Comment request schema](assets/comment_cli_req.schema.json)
- [Comment response schema](assets/comment_cli_resp.schema.json)
- [Hot list response schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON results from the skill commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output is intended to be JSON on stdout; logs and status messages may be written separately, and result datasets may be saved locally.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
