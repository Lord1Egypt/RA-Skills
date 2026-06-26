## Description: <br>
Aggregates domestic and international society, technology, and military news, then searches, filters, organizes, and summarizes key highlights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouhuihui008](https://clawhub.ai/user/zhouhuihui008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to collect current society, technology, and military news from named public sources and receive a structured Markdown digest with links, sources, timestamps, and key points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Breaking and military news can contain outdated, duplicated, or unverified claims. <br>
Mitigation: Check the cited source links, publication timestamps, and corroboration from trusted outlets before using the summary for decisions. <br>
Risk: Version metadata is inconsistent between server release metadata and artifact frontmatter. <br>
Mitigation: Treat the server release version as the release identifier and confirm artifact version metadata before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouhuihui008/hot-news-aggregator-1-0-0) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [TechCrunch](https://techcrunch.com) <br>
- [The Verge](https://www.theverge.com) <br>
- [Wired](https://www.wired.com) <br>
- [Defense News](https://www.defensenews.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Analysis] <br>
**Output Format:** [Structured Markdown news digest with linked headlines, source names, timestamps, and summarized key points] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires fresh web search or fetch results; outputs should preserve source links and timestamps for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/_meta.json; artifact/SKILL.md frontmatter lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
