## Description:

Provides command-line access to Xiaohongshu public search, note detail, comment, and creator-post data so agents can return structured JSON for trend, content, competitor, KOL, and sentiment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, marketers, and data analysts use this skill to collect public Xiaohongshu search results, note details, comments, and creator posts for topic research, competitive monitoring, KOL screening, trend tracking, and audience-feedback analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the primary description understates broader search, profile, and detail capabilities.

Mitigation: Install and use it only when the broader Xiaohongshu trend, search, detail, comment, and creator-post workflow is intended.

Risk: The skill uses a Guaikei API token and the security guidance warns users to review token handling.

Mitigation: Use a scoped GUAIKEI_API_TOKEN where possible and rotate tokens used with this version.

Risk: Command results can be written to a local logs directory, which may expose collected data in shared or synced workspaces.

Mitigation: Run in an appropriate workspace, avoid shared or synced directories for sensitive analysis, and clear logs after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-trend-insights)
- [Guaikei API site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Node.js 16.14.0+ and GUAIKEI_API_TOKEN; successful runs may save JSON result files under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
