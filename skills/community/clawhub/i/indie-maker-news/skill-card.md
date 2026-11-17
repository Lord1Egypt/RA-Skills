## Description:

Indie Maker News helps agents fetch and filter public news, RSS, and API items about solo businesses, side projects, startups, and monetization opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylnwu](https://clawhub.ai/user/kylnwu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a Chinese news aggregation workflow that surfaces monetization-related startup, side-project, and independent-maker items from public sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts public news, RSS, and API sources despite stale artifact documentation claiming local-only or no external API behavior.

Mitigation: Tell users to expect outbound requests to public news sources and update stale local-only claims before publishing.

Risk: Aggregated news and keyword-filtered summaries may be incomplete, stale, or misleading for business decisions.

Mitigation: Review source links and corroborate important claims before acting on monetization or startup guidance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kylnwu/skills/indie-maker-news)
- [36Kr RSS Feed](https://36kr.com/feed)
- [Huxiu RSS Feed](https://www.huxiu.com/rss/0.xml)
- [V2EX RSS Feed](https://www.v2ex.com/index.xml)
- [Hacker News RSS Feed](https://hnrss.org/frontpage)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Chinese text summaries and structured JSON news items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Aggregates public news sources and filters items by monetization-related keywords.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
