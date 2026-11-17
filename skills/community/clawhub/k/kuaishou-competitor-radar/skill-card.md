## Description:

This skill compares public Kuaishou videos, creator posts, and comments to help assess brand performance, engagement, discussion trends, and actionable opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Marketing, research, and brand teams use this skill to compare public Kuaishou content and engagement, review changes over time, understand video discussions, and identify content opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and identifiers leave the local device and are sent to the service.

Mitigation: Use a Guaikei-issued token, avoid confidential search terms, and review the provider's charges and data-retention terms.

Risk: Optional logging stores queries and returned data locally.

Mitigation: Enable logging only when needed and handle the resulting local files according to their sensitivity.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/kuaishou-competitor-radar)
- [Guaikei service and access](https://www.guaikei.com)
- [Command options](references/options.md)
- [Release changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON data, Analysis]

**Output Format:** [JSON response envelopes containing video, creator, or comment records and engagement metrics; agent-facing summaries and comparisons can be written in text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries and identifiers are sent to the disclosed service. Public Kuaishou data only; monthly token limits are 30 search results, 50 creator posts, and 60 comments. Results are not saved locally by default; optional logging is available.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter, package.json, changelog; released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
