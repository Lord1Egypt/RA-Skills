## Description:

Collects public Kuaishou videos, creator posts, comments, and engagement metrics through keyword, profile, or video-link queries, returning structured data for content research and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Kuaishou creators, marketers, and analysts can search public videos, review a creator’s public posts, and examine video comments and engagement metrics to support content planning, competitor research, and audience analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and video or profile links are sent to the GUAIKEI third-party service.

Mitigation: Avoid submitting confidential queries or links, and use the service only when that data sharing is acceptable.

Risk: Security analysis was incomplete for some skill components.

Mitigation: Review the skill before installation and use, especially if it will handle sensitive workflows.

## Reference(s):

- [Command options](references/options.md)
- [GUAIKEI service and token access](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON results with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on whether the request searches videos, retrieves creator posts, or retrieves comments; engagement counts may be numeric or strings.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter, package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
