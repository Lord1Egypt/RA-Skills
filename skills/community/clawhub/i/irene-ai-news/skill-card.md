## Description:

Daily AI news aggregator that fetches AI-related content from HackerNews, GitHub Trending, ArXiv papers, and configured web search sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chyher](https://clawhub.ai/user/chyher)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to generate a daily AI digest, track trending AI projects, and discover recent AI research from public sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes public network requests to gather news, repository, paper, and optional search results.

Mitigation: Review the configured sources before installation and run it only in environments where those outbound requests are acceptable.

Risk: Automated channel posting can target an ambiguous destination when configured to use the last contacted channel.

Mitigation: Configure an explicit destination channel and test the command without scheduled delivery before enabling cron.

Risk: Credential setup examples can expose API keys if real secrets are pasted into shell commands or history.

Mitigation: Store API keys through a protected environment or secret-management workflow and avoid echoing real keys in commands.

Risk: The documentation claims Brave/Tavily web-search support, while the bundled script may not fully implement that path.

Mitigation: Verify search-provider behavior and review or pin any separate Tavily community skill before relying on web-search results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chyher/skills/irene-ai-news)
- [Tavily](https://tavily.com/)
- [Hacker News Algolia API](https://hn.algolia.com/api)
- [GitHub Search Repositories API](https://docs.github.com/en/rest/search/search?apiVersion=2022-11-28#search-repositories)
- [arXiv API](https://info.arxiv.org/help/api/index.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown digest by default, with optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output is generated from public news, repository, and paper sources and can optionally be posted to an OpenClaw channel.]

## Skill Version(s):

1.1.0 (source: server release, frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
