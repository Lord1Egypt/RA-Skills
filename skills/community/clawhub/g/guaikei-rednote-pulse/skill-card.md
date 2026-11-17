## Description:

Retrieves public Xiaohongshu content through keyword search, note detail lookup, comment extraction, and creator post listing, returning structured JSON for topic research, competitor monitoring, KOL screening, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content creators, marketers, analysts, and operations teams use this skill to collect public Xiaohongshu notes, comments, and creator post data for content planning, market research, competitive tracking, KOL screening, and sentiment review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, URLs, and a GUAIKEI_API_TOKEN to Guaikei.

Mitigation: Use it only for data you are allowed to disclose to Guaikei, keep the token in a local environment variable, and rotate the token if it is exposed.

Risk: Fetched results are automatically saved in local logs.

Mitigation: Avoid shared or synced workspaces for sensitive research and delete generated logs when they are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-rednote-pulse)
- [Guaikei API Access and Support](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with command examples and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; command results may be saved to local logs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata declares 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
