## Description: <br>
Daily AI news aggregator that fetches latest AI-related content from HackerNews, GitHub Trending, ArXiv papers, and web search providers such as Brave or Tavily. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chyher](https://clawhub.ai/user/chyher) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and teams use this skill to collect a daily AI news digest from public technical, open-source, research, and web-search sources. It can print the digest locally, return JSON, or send the digest to an OpenClaw channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled sends can post a digest to an unintended destination if configured to use the last-contacted channel. <br>
Mitigation: Configure cron or --send with a fixed, verified channel before enabling automated posting. <br>
Risk: Adding Tavily or Brave search introduces API-key handling outside the base skill. <br>
Mitigation: Review the separate search-provider integration and store API keys only in the intended OpenClaw environment configuration. <br>
Risk: The digest depends on public feeds and search results that can be incomplete, unavailable, or stale. <br>
Mitigation: Treat the digest as a starting point and verify important items through the linked source material before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chyher/irene-ai-news) <br>
- [Publisher profile](https://clawhub.ai/user/chyher) <br>
- [Tavily](https://tavily.com/) <br>
- [Hacker News Algolia API](https://hn.algolia.com/api/v1/search_by_date) <br>
- [GitHub repository search API](https://api.github.com/search/repositories) <br>
- [ArXiv API](http://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration] <br>
**Output Format:** [Markdown daily digest by default, JSON when invoked with --json, and optional OpenClaw channel message when invoked with --send.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public news and research sources over the network; output freshness depends on source availability and provider configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
