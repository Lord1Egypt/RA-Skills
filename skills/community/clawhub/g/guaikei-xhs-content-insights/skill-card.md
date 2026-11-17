## Description:

Xiaohongshu Content Insights retrieves public Xiaohongshu search results, note details, comments, and creator posts as structured JSON for trend, content, competitor, KOL, and sentiment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, marketing teams, data analysts, and business operators use this skill to collect public Xiaohongshu content data for topic research, trend monitoring, competitor tracking, KOL screening, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens, searched topics, Xiaohongshu links, comments, profile data, and generated logs may be sensitive.

Mitigation: Use only where sending targets to Guaikei and retaining local logs are approved; avoid committing or sharing generated logs.

Risk: The server security verdict is suspicious and recommends review before installation.

Mitigation: Review the skill before installing, especially token handling, access-bearing URLs, and saved result files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-content-insights)
- [Guaikei API Service](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Structured JSON with concise human-facing status and error guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; successful runs may save JSON results under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
