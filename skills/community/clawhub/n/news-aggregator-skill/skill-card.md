## Description: <br>
News Aggregator Skill fetches, filters, and analyzes current items from Hacker News, GitHub Trending, Product Hunt, 36Kr, Tencent News, WallStreetCN, V2EX, and Weibo for briefings and topic scans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cclank](https://clawhub.ai/user/cclank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and other external users use this skill to collect current technology, finance, open source, and social trend items from multiple public sources and turn them into concise Chinese briefings or deeper topic scans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts multiple public news sites and, in deep mode, follows article links for full-text extraction. <br>
Mitigation: Use narrower sources or keywords, avoid deep mode when lower network exposure is needed, and run in an environment with appropriate network controls. <br>
Risk: Fetched article text is untrusted web content and may be inaccurate, stale, or adversarial. <br>
Mitigation: Treat fetched content as source material for review and verify important claims before relying on them. <br>
Risk: Generated Markdown reports are saved locally and may include third-party article content. <br>
Mitigation: Review report contents and storage location before sharing, retaining, or using them in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cclank/news-aggregator-skill) <br>
- [Publisher profile](https://clawhub.ai/user/cclank) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [JSON arrays from the fetch script and Chinese Markdown reports presented in chat and saved as timestamped files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional deep mode adds fetched article text; reports are saved under reports/.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
