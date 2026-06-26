## Description: <br>
Comprehensive news aggregator that fetches, filters, and deeply analyzes real-time content from 8 major sources: Hacker News, GitHub Trending, Product Hunt, 36Kr, Tencent News, WallStreetCN, V2EX, and Weibo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonyliu9189](https://clawhub.ai/user/tonyliu9189) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to fetch current news from major technology, finance, social, and Chinese-language sources, then produce concise Chinese briefings with links, metadata, and deeper interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches and parses external news pages, which may contact sites outside an organization's expected network boundary. <br>
Mitigation: Review or restrict the configured source list before installation when network destinations must be controlled. <br>
Risk: Reports are saved locally and may include article text or summaries from external pages. <br>
Mitigation: Confirm the report output directory and retention practices fit the deployment environment before routine use. <br>
Risk: The skill defaults final reports to Simplified Chinese, which may not match every reader's language expectations. <br>
Mitigation: Override or modify the response language guidance when users need reports in another language. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tonyliu9189/news-aggregator-skill-2) <br>
- [Publisher profile](https://clawhub.ai/user/tonyliu9189) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown reports with source links, metadata, summaries, interpretation bullets, and timestamped report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can fetch external news pages, optionally include extracted article content as JSON from its helper script, and defaults final reports to Simplified Chinese.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
