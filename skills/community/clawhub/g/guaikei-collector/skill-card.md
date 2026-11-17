## Description:

xhs public data collection helper for keyword note search, note details and comments, and creator post monitoring, returning structured data for topic research and competitive analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Marketers, content creators, analysts, and agent workflows use this skill to collect public Xiaohongshu notes, comments, and creator posts for content planning, competitive research, trend monitoring, and report preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, note or profile URLs, and the Guaikei API token are sent to the Guaikei service during normal operation.

Mitigation: Use the skill only when that data sharing is acceptable, and avoid submitting sensitive research targets or credentials outside approved environments.

Risk: Generated logs can contain research targets, collected comments, profile or note URLs, and xsec_token-bearing links.

Mitigation: Treat logs as sensitive artifacts; restrict access on shared systems and delete or retain them according to the user's data-handling policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-collector)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON results from the command-line tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Node.js 16.14.0+ and GUAIKEI_API_TOKEN; results may be saved under logs/.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
