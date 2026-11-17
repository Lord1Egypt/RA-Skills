## Description:

Retrieves public Douyin data for keyword searches, creator posts, video comments, and trending topics, while excluding other platforms and account-growth advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and marketing teams use this skill to run Douyin keyword, creator-post, comment, and hot-list queries through Node.js CLI commands and receive structured JSON for content research, competitor monitoring, sentiment review, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin public data is sent to Guaikei's API and returned as full JSON.

Mitigation: Use the skill only when this data transfer is intended, and avoid submitting sensitive or private content.

Risk: Broad comment or creator collection can save large public-data results locally.

Mitigation: Limit query scope, review permissions for the intended use, and control access to generated logs.

Risk: GUAIKEI_API_TOKEN is sensitive and token or error handling was flagged for review.

Mitigation: Store the token only in a protected environment variable, rotate it if exposed, and review authentication behavior before deployment.

Risk: Broad triggering can run data collection when the user's intent is ambiguous.

Mitigation: Confirm the user wants Douyin public-data retrieval before running search, creator, or comment commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-query-retrieve-deliver-public-data)
- [Guaikei Service Website](https://www.guaikei.com)
- [Options Reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)
- [Input and Output JSON Schemas](artifact/assets/)

## Skill Output:

**Output Type(s):** [shell commands, JSON, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI stdout and saved logs are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; writes JSON results to local logs.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, changelog, skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
