## Description: <br>
Daily industry news tracking assistant that fetches recent technology media articles from RSS feeds, filters them by configurable keywords and sources, and produces a concise digest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongrebeccahhh-boop](https://clawhub.ai/user/dongrebeccahhh-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and news-monitoring users can use this skill to collect recent RSS articles from configured technology, finance, and science sources, filter them by include and exclude keywords, and review a dated digest with titles, summaries, source names, and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional cron setup creates recurring background network activity against configured RSS sources. <br>
Mitigation: Review the script, RSS sources, and delivery expectations before enabling the scheduled task; run the skill manually if background activity is not desired. <br>
Risk: The digest depends on external RSS feeds and user-configured sources, so results may be incomplete, unavailable, or include source-provided errors. <br>
Mitigation: Confirm the configured sources are expected and review article links and summaries before relying on the digest. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dongrebeccahhh-boop/industry-news-agent) <br>
- [36Kr RSS feed](https://36kr.com/feed) <br>
- [Huxiu RSS feed](https://www.huxiu.com/rss/0.xml) <br>
- [Leiphone RSS feed](https://www.leiphone.com/feed) <br>
- [ScienceDaily RSS feed](https://www.sciencedaily.com/rss/all.xml) <br>
- [Nature RSS feed](https://www.nature.com/nature.rss) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown-formatted news digest printed to stdout, with optional shell commands and YAML configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filters RSS articles from configured sources by recency and keywords; result limits are configurable.] <br>

## Skill Version(s): <br>
3.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
