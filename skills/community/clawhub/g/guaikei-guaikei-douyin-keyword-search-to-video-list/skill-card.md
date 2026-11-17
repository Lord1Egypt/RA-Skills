## Description:

Retrieves public Douyin data for keyword search, creator post lists, video comments, and hot-topic lists to support content research, competitor analysis, sentiment monitoring, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect structured public Douyin search results, creator videos, comments, and hot topics through Node.js CLI commands for downstream analysis and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin queries, target URLs or IDs, and GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Use only approved data and tokens, confirm that third-party API sharing is acceptable for the workspace, and avoid submitting confidential or sensitive targets.

Risk: The API token is sent in URL query strings.

Mitigation: Treat command output, logs, shell history, and network traces as sensitive; rotate GUAIKEI_API_TOKEN if it may have been exposed.

Risk: Successful search, creator-post, and comment results are saved locally under the skill's logs directory by default.

Mitigation: Review retention needs, restrict access to the logs directory, and delete saved result files when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-guaikei-douyin-keyword-search-to-video-list)
- [Guaikei API website](https://www.guaikei.com)
- [Complete options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search CLI request schema](assets/search_cli_req.schema.json)
- [Search CLI response schema](assets/search_cli_resp.schema.json)
- [Post CLI response schema](assets/post_cli_resp.schema.json)
- [Comment CLI response schema](assets/comment_cli_resp.schema.json)
- [Hot topics CLI response schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with Node.js CLI commands and structured JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands write pure JSON to stdout, send logs to stderr, and may save successful results under the skill's logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
