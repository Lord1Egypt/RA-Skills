## Description:

Fetches public Kuaishou video search results, creator post lists, and video comments through the Guaikei API, returning structured JSON for content research, competitor monitoring, KOL discovery, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, analysts, and agent operators use this skill to collect public Kuaishou keyword, creator, and comment data for content planning, competitor monitoring, audience research, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, target account URLs, video URLs, and collected comments are sent to www.guaikei.com using the configured API token.

Mitigation: Avoid confidential research targets unless external API processing is acceptable, and review token handling before installation.

Risk: Full collected results are automatically saved as plaintext JSON files under logs without documented retention controls.

Mitigation: Protect or delete generated log files after use, and avoid running the skill where local result retention is unacceptable.

Risk: The server security verdict is suspicious because of local plaintext result storage behavior.

Mitigation: Review the skill before deployment and limit use to public Kuaishou data collection scenarios covered by the documentation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-hashtag-video-fetcher)
- [Publisher Profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API Service](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and can save full result JSON files locally under logs.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
