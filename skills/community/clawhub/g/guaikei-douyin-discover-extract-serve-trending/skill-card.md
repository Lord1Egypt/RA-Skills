## Description:

Finds public Douyin videos, creator posts, comments, and trending topics through Node.js CLI commands that return structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and analysts use this skill to search public Douyin content, monitor creator posts, retrieve comments, and inspect trending lists for content research and social listening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, profile/video URLs, and GUAIKEI_API_TOKEN are sent to www.guaikei.com.

Mitigation: Use only when that data transfer is acceptable, scope the token for this service, and avoid submitting sensitive or private identifiers.

Risk: Generated logs may retain scraped public data, including personal information in comments or profiles.

Mitigation: Treat logs as retained scraped data, limit access, and delete or redact them when they are no longer needed.

Risk: The skill can activate for ambiguous short-video research requests even when Douyin is not explicitly named.

Mitigation: Ask for confirmation before collection when the user has not clearly requested Douyin data.

Risk: Runtime authentication errors may include promotional contact output that contradicts the skill documentation.

Mitigation: Review or patch authentication-error messages before use in managed or customer-facing environments.

Risk: Some response schemas include video playback or download URLs, while the skill says it is not for video-download workflows.

Mitigation: Do not use the skill to download videos, and filter or suppress download links when they are not required for analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-discover-extract-serve-trending)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei token and support site](https://www.guaikei.com)
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

**Output Type(s):** [text, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI stdout is JSON and generated logs are JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14.0 and GUAIKEI_API_TOKEN; command results may include public Douyin profile URLs, video URLs, comments, and trend data.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, SKILL.md frontmatter, references/changelog.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
