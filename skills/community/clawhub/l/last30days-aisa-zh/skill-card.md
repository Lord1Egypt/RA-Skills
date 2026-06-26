## Description: <br>
Aggregates recent Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, and grounded web results into last-30-days research briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research users use this skill to collect and synthesize recent social, community, prediction-market, GitHub, and web signals about people, companies, products, competitors, releases, and trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and snippets may be sent to external AISA-backed research services. <br>
Mitigation: Install and run only when external processing is acceptable for the research topic; avoid sensitive topics unless the service path is approved. <br>
Risk: Watchlist features can retain topics and findings locally. <br>
Mitigation: Review or avoid watchlist use when local retention is not desired, and clear stored data according to the user's retention policy. <br>
Risk: Webhook notifications can expose sensitive research topics or findings to configured destinations. <br>
Mitigation: Configure delivery webhooks only for trusted destinations and avoid using them for sensitive research. <br>
Risk: The Xiaohongshu source may contact a local service when requested. <br>
Mitigation: Use that source only when the local service is expected and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/last30days-aisa-zh) <br>
- [Publisher profile](https://clawhub.ai/user/bibaofeng) <br>
- [Declared repository in artifact metadata](https://github.com/AIsa-team/agent-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, compact text, JSON reports, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit compact Markdown or structured JSON with query plans, ranked candidates, clusters, and items grouped by source.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
