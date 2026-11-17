## Description:

Makima's All-Seeing Intelligence Suite combines real-time AI news tracking and global news monitoring for a comprehensive strategic briefing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhrisfu](https://clawhub.ai/user/xhrisfu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to collect recent AI and global news signals from RSS feeds, news APIs, and selected article pages for briefing and synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article links can lead requests outside the declared news-source network scope.

Mitigation: Run the skill with restricted network egress and allow only the intended source domains and reviewed article destinations.

Risk: Scraped article text is untrusted source material that may be incomplete, misleading, or prompt-injection shaped.

Mitigation: Treat collected snippets as evidence for summarization only, and avoid giving the consuming agent secrets or high-impact tools during synthesis.

Risk: JavaScript dependencies are declared without a lockfile in the artifact evidence.

Mitigation: Pin dependencies with a lockfile and review dependency updates before installing or running the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xhrisfu/skills/intelligence-suite)
- [OpenAI Blog RSS](https://openai.com/blog/rss.xml)
- [Microsoft AI Blog RSS](https://blogs.microsoft.com/ai/feed/)
- [Reuters Agency Feed](https://www.reutersagency.com/feed/?best-regions=global&post_type=best)
- [SCMP China/HK RSS](https://www.scmp.com/rss/91/feed)
- [RTHK Local News RSS](https://rthk9.rthk.hk/rthk/news/rss/e_expressnews_elocal.xml)
- [Hacker News Top Stories API](https://hacker-news.firebaseio.com/v0/topstories.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Console text structured as intelligence packs for agent synthesis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches recent feed items, scrapes article snippets, and truncates scraped content before handing it to the consuming agent.]

## Skill Version(s):

1.0.3 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
