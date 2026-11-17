## Description:

Makima's All-Seeing Intelligence Suite combines real-time AI news tracking and global news monitoring for strategic briefings, with LLM analysis powered by SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to gather recent AI and global news signals, scrape article snippets, and produce structured strategic briefings through an LLM analysis step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill sends the configured API key and scraped article content to an undeclared API host.

Mitigation: Review before installing, confirm the intended API hostname with the publisher, and use only if sending SKILLBOSS_API_KEY and scraped news excerpts to that endpoint is acceptable.

Risk: The security summary says article URLs are fetched without enough network scoping.

Mitigation: Run the skill in a network-restricted environment or patch URL allowlisting before use.

Risk: The security guidance notes that dependencies are not pinned with a lockfile.

Mitigation: Prefer pinned dependencies and a reviewed lockfile before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marjoriebroad/skills/intelligence-suite-2)
- [Publisher Profile](https://clawhub.ai/user/marjoriebroad)
- [SkillBoss Skill Listing](https://skillboss.co/skills/intelligence-suite)
- [SkillBoss API Endpoint Used by Artifact](https://api.heybossai.com/v1)
- [OpenAI Blog RSS](https://openai.com/blog/rss.xml)
- [Microsoft AI Blog RSS](https://blogs.microsoft.com/ai/feed/)
- [Hacker News Firebase API](https://hacker-news.firebaseio.com/v0/topstories.json)
- [Reuters Agency Feed](https://www.reutersagency.com/feed/?best-regions=global&post_type=best)
- [SCMP RSS Feed](https://www.scmp.com/rss/91/feed)
- [RTHK RSS Feed](https://rthk9.rthk.hk/rthk/news/rss/e_expressnews_elocal.xml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text with structured news packs and optional LLM-generated briefing prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, and SKILLBOSS_API_KEY for LLM analysis; without the key, the scripts print collected news packs and skip LLM analysis.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
