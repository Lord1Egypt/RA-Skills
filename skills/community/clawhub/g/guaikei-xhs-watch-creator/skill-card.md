## Description:

Retrieves public Xiaohongshu posts, note details, comments, and creator posts through Guaikei command-line tools for content, trend, competitor, and audience analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, brand marketers, and analysts use this skill to retrieve Xiaohongshu public data for keyword research, note review, comment analysis, creator monitoring, competitor tracking, KOL screening, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu URLs, keywords, and GUAIKEI_API_TOKEN to guaikei.com.

Mitigation: Use the skill only when this data sharing is authorized, and prefer a limited or revocable API token.

Risk: Retrieved datasets may be written to local JSON log files.

Mitigation: Treat generated logs as sensitive, avoid synced or shared folders, and delete artifact/logs outputs when no longer needed.

Risk: The security verdict is suspicious because the skill handles an API credential and stored datasets.

Mitigation: Review the skill and its data-handling behavior before installing or running it in a production workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-watch-creator)
- [Guaikei API site](https://www.guaikei.com)
- [Options and invocation guide](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; command results are JSON and may also be saved as JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; command outputs include status, error_code, request metadata, skill metadata, and results.]

## Skill Version(s):

1.0.0 (source: server release metadata and server release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
