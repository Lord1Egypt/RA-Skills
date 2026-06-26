## Description: <br>
Multi-source search skill for Kiro on OpenClaw. Aggregate and rank results from Google, Google Scholar, YouTube, and X, then output a concise brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vmining](https://clawhub.ai/user/Vmining) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and knowledge workers use this skill to collect and rank search results across web, scholarly, video, and X sources, then generate a concise search brief for a query. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to external providers when their sources are selected. <br>
Mitigation: Avoid sensitive internal, personal, regulated, or secret-bearing queries, and omit credentials for providers you do not intend to use. <br>
Risk: Generated latest.json and latest.md files may retain private or sensitive search results locally. <br>
Mitigation: Review, protect, or delete generated result files when queries or results may contain private information. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Vmining/kiro-search-aggregator) <br>
- [Publisher profile](https://clawhub.ai/user/Vmining) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Serper API endpoint](https://google.serper.dev) <br>
- [SerpAPI search endpoint](https://serpapi.com/search.json) <br>
- [X recent search endpoint](https://api.x.com/2/tweets/search/recent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Console JSON plus local latest.json and latest.md files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes results to outputs/search-aggregator by default and ranks merged results by source, recency, and result position signals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
