## Description:

Retrieves public Douyin search results, creator posts, comments, and hot-ranking data through Guaikei API commands for downstream content, marketing, trend, and competitor analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and content operations teams use this skill to run Node.js commands that collect structured public Douyin data for keyword research, hot-topic tracking, creator monitoring, comment analysis, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin search terms, creator or video URLs, and GUAIKEI_API_TOKEN to guaikei.com.

Mitigation: Use only an approved token, treat it as sensitive, and avoid sensitive searches or URLs on shared or synced machines.

Risk: The security summary states that full results are stored locally by default.

Mitigation: Review and clear the generated logs directory after use, especially when results may contain sensitive business, creator, or campaign research.

Risk: The security summary notes that returned data may expose playback or download URL fields even though the skill says downloads are unsupported.

Mitigation: Use returned media-link fields only when they fit applicable legal, platform, and organizational obligations; do not use the skill for unauthorized downloading or redistribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-get-hot-ranking)
- [engheng-art publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API website](https://www.guaikei.com)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)
- [Search request schema](artifact/assets/search_cli_req.schema.json)
- [Search response schema](artifact/assets/search_cli_resp.schema.json)
- [Hot ranking response schema](artifact/assets/hot_cli_resp.schema.json)
- [Post request schema](artifact/assets/post_cli_req.schema.json)
- [Post response schema](artifact/assets/post_cli_resp.schema.json)
- [Comment request schema](artifact/assets/comment_cli_req.schema.json)
- [Comment response schema](artifact/assets/comment_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0 or later and GUAIKEI_API_TOKEN; successful search, post, and comment commands also write JSON logs under the skill logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json, references/changelog.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
