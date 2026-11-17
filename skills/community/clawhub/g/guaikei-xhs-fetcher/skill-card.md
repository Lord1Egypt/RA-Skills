## Description:

Fetches structured public Xiaohongshu note, comment, keyword search, and creator post data for content research, competitor monitoring, KOL screening, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, marketing teams, analysts, and developers use this skill to retrieve structured public Xiaohongshu data for topic discovery, competitor review, KOL assessment, comment analysis, and downstream reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends GUAIKEI_API_TOKEN, Xiaohongshu URLs, search terms, and fetched datasets to a third-party API service.

Mitigation: Use the skill only when guaikei.com is an approved service, use a limited and rotatable token, and avoid sensitive research targets unless collection is authorized.

Risk: Successful runs may save full result JSON locally under logs/.

Mitigation: Store generated logs only in approved locations, delete them when no longer needed, and do not commit or share the logs/ directory.

Risk: The server security verdict is suspicious because the skill performs third-party data egress and local result persistence.

Mitigation: Review and scan before installation, and confirm the intended data collection and retention practices are acceptable for the deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-fetcher)
- [Publisher Profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API Service](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and structured JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; successful runs may save full result JSON under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
