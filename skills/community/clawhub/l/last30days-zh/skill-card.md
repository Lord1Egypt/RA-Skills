## Description: <br>
Aggregates recent Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, and web search results from the last 30 days into a research brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research recent topics, companies, products, markets, tools, trends, competitor activity, launch reactions, and community sentiment across multiple social, community, prediction-market, and web sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics and public-result snippets may be sent to AISA and other enabled public-data services. <br>
Mitigation: Install and run the skill only when those external lookups are acceptable for the topic and deployment context. <br>
Risk: The skill requires an AISA API key. <br>
Mitigation: Keep the AISA key scoped, provide it through the documented environment variable or config file, and store ./.last30days-data/config.env with restrictive permissions. <br>
Risk: Optional source expansions can increase the number of external lookups. <br>
Mitigation: Avoid enabling optional YouTube transcripts, auto-resolve, Xiaohongshu, Threads, or Pinterest lookups unless those additional retrievals are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/last30days-zh) <br>
- [AISA](https://aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, compact text, or structured JSON depending on the selected emit mode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit compact summaries, full Markdown reports, contextual summaries, or JSON with query plans, ranked candidates, clusters, and source-grouped items.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
