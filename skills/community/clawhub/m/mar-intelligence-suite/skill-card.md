## Description:

Makima's All-Seeing Intelligence Suite combines real-time AI news tracking and global news monitoring into a strategic briefing with LLM analysis powered by SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to gather recent AI and global news signals, scrape short article snippets, and produce structured strategic briefings through an LLM analysis service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the required API key and scraped article snippets to api.heybossai.com, which differs from the declared api.skillboss.com permission.

Mitigation: Use a narrowly scoped, revocable API key and approve outbound access to the actual analysis endpoint before running.

Risk: Feed-controlled article links may cause requests to unexpected URLs, including private-network targets.

Mitigation: Run the skill in a network-restricted environment with egress controls and review fetched source links before execution where practical.

Risk: Generated briefings may contain untrusted summaries, and one monitor entry is hardcoded mock data.

Mitigation: Treat the briefing as advisory, verify important claims against primary sources, and account for mock entries during review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marjoriebroad/skills/mar-intelligence-suite)
- [SkillBoss Intelligence Suite Page](https://skillboss.co/skills/intelligence-suite)
- [SkillBoss API Hub Endpoint](https://api.heybossai.com/v1)
- [OpenAI Blog RSS](https://openai.com/blog/rss.xml)
- [Microsoft AI Blog RSS](https://blogs.microsoft.com/ai/feed/)
- [Reuters Agency Feed](https://www.reutersagency.com/feed/?best-regions=global&post_type=best)
- [SCMP China RSS Feed](https://www.scmp.com/rss/91/feed)
- [RTHK Local News RSS Feed](https://rthk9.rthk.hk/rthk/news/rss/e_expressnews_elocal.xml)
- [Hacker News Top Stories API](https://hacker-news.firebaseio.com/v0/topstories.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Console text with structured briefing sections and optional LLM-generated analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, network access, and SKILLBOSS_API_KEY for LLM analysis; without the key it prints gathered packs and skips LLM analysis.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
