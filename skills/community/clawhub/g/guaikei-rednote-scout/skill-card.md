## Description:

Provides structured Xiaohongshu (Rednote) public-data retrieval for keyword discovery, competitor monitoring, KOL screening, creator post monitoring, and comment insight workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, marketers, analysts, and agents use this skill to collect structured public Xiaohongshu search, note, creator-post, and comment data for downstream research, reporting, and content-planning decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GUAIKEI_API_TOKEN and request inputs are sent to guaikei.com, and the security evidence notes token transmission in URL parameters.

Mitigation: Install only when this data flow is acceptable, provision the token through an official path, keep the token secret, and rotate it if exposed.

Risk: Generated logs may contain research queries, public profile or comment data, and xsec_token-bearing Xiaohongshu URLs.

Mitigation: Store logs in a protected location, periodically delete unneeded logs, and avoid sharing raw output outside the authorized team.

Risk: The skill collects public platform data for marketing and research workflows, which can be misused if redistributed or applied outside the user's authorization scope.

Mitigation: Use the skill only for public data and authorized internal analysis, and review applicable platform, privacy, and distribution restrictions before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-rednote-scout)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Node.js 16.14.0+ and GUAIKEI_API_TOKEN; results may be saved locally under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
