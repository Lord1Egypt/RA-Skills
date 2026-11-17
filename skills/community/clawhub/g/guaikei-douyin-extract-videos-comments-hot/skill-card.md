## Description:

Collects public Douyin data for keyword search, author posts, video comments, and real-time hot lists for content research, competitor analysis, comment insight, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content, marketing, and operations teams use this skill to query public Douyin videos, authors, comments, and hot list data for content research, competitor analysis, audience feedback review, and trend monitoring.

### Deployment Geography for Use:

China-focused

## Known Risks and Mitigations:

Risk: Douyin search terms, account or video targets, and the Guaikei API token are sent to the Guaikei service.

Mitigation: Use only with approved targets and an account/token intended for this workflow; rotate the token if it may have been exposed.

Risk: Collected Douyin results may be saved locally under logs by default.

Mitigation: Avoid shared, synced, CI, or sensitive workspaces unless retention is controlled; review and remove logs that should not persist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-extract-videos-comments-hot)
- [Guaikei data service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Structured JSON from CLI commands, with optional Markdown summaries by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; collected results may be saved locally under logs by default.]

## Skill Version(s):

1.0.0 (source: release evidence, package.json, and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
