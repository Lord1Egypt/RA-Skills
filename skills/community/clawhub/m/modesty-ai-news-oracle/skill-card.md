## Description:

Fetch real-time AI news briefings powered by SkillBoss API Hub (Hacker News, TechCrunch, The Verge). Uses SkillBoss search and chat capabilities for news aggregation and summarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to fetch current AI news briefings from SkillBoss-powered search and chat flows, including summarized items and source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation identity and authoritative source may be inconsistent.

Mitigation: Verify the ClawHub publisher and authoritative repository before installation, and prefer a pinned reviewed release or registry package.

Risk: Briefing requests use a third-party SkillBoss API key and may expose sensitive context if included in prompts.

Mitigation: Avoid sending secrets or private internal context through the briefing flow, and use a scoped SkillBoss API key when available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/modestyrichards/skills/modesty-ai-news-oracle)
- [SkillBoss Setup Guide](https://skillboss.co/skill.md)
- [SkillBoss API Hub Endpoint](https://api.skillboss.co/v1/pilot)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Text briefing or structured JSON with timestamps, summarized news items, and source links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; output depends on third-party SkillBoss API availability and retrieved news sources.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
