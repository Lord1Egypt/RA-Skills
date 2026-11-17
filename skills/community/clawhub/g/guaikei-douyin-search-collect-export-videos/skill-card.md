## Description:

This skill helps an agent collect public Douyin data through CLI commands for keyword search, creator post collection, video comment retrieval, and real-time hot-list lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content researchers, marketers, and developers use this skill to research public Douyin videos, creators, comments, and trending topics for content planning, competitor analysis, user insight, and trend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin search terms, URLs, and the Guaikei API token are sent to www.guaikei.com.

Mitigation: Install only when that data sharing is acceptable, keep the token in the environment, and rotate it if it may have been exposed.

Risk: Saved logs may contain collected public account, video, and comment data.

Mitigation: Review, protect, or delete files under logs/ according to the user's data retention needs.

Risk: Broad activation rules and returned media URL fields may encourage out-of-scope downloading or redistribution.

Mitigation: Use the skill only for public-data research workflows and avoid download, reposting, or distribution use cases.

Risk: Authentication error paths may display support or contact information despite documentation describing neutral runtime errors.

Mitigation: Review authentication failure behavior before deployment and avoid exposing stderr directly to end users when that disclosure is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-search-collect-export-videos)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Request and response schemas](assets/)
- [Guaikei website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, files, guidance]

**Output Format:** [CLI guidance plus structured JSON stdout, stderr status messages, and saved JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 16.14.0 and GUAIKEI_API_TOKEN. Results are limited to public Douyin data and may be written under logs/.]

## Skill Version(s):

1.0.0 (source: SKILL.md metadata, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
