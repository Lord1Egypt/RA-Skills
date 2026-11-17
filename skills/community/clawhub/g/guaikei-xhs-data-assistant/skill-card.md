## Description:

Provides Xiaohongshu public data workflows for note search, note details, comments, and creator post monitoring, returning structured results for content, competitor, KOL, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, marketers, and analysts use this skill to collect and summarize public Xiaohongshu notes, comments, and creator posts for topic research, competitor monitoring, KOL screening, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, URLs, and GUAIKEI_API_TOKEN to Guaikei.

Mitigation: Use the skill only when that data sharing is acceptable, treat GUAIKEI_API_TOKEN as a secret, and rotate the token if it may have been exposed.

Risk: Fetched outputs may be saved locally and can include comments, business research, and signed Xiaohongshu links.

Mitigation: Review the logs/ directory after use and delete retained outputs that should not remain on disk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-data-assistant)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON result interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; fetched results may be saved locally under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
