## Description:

Retrieves public Xiaohongshu keyword results, note details, author post lists, and comments through Node.js CLI commands for market research and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External developers, analysts, marketers, and content operators use this skill to collect public Xiaohongshu keyword, note, author, and comment data for trend research, competitor monitoring, KOL screening, and downstream reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, URLs, and public-data requests are sent to guaikei.com with a GUAIKEI_API_TOKEN.

Mitigation: Use the skill only when that data sharing is acceptable, scope requests to public data, and rotate the token if request URLs or logs may have been exposed.

Risk: Generated local logs may contain sensitive market-research artifacts or request details.

Mitigation: Review log retention practices and delete generated logs when they are no longer needed.

## Reference(s):

- [Complete Options](references/options.md)
- [Changelog](references/changelog.md)
- [Guaikei Service](https://www.guaikei.com)
- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-market-research)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with Node.js shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may save local JSON logs under the skill's logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
