## Description: <br>
Tracks public hot topics across major Chinese social and content platforms, removes noisy or promotional items, and ranks the default Top 10 by discussion, reach, sharing, emotion, contention, timeliness, and cross-platform coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[e2e5g](https://clawhub.ai/user/e2e5g) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content teams, and analysts use this skill to monitor public trend data, cluster related topics, down-rank low-value noise, and produce neutral hot-topic rankings or trend reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live public trend data can be stale, incomplete, platform-skewed, or unavailable in the execution environment. <br>
Mitigation: Name the platforms and time window when precision matters, prefer offline snapshots when needed, and label whether results come from live collection or local data. <br>
Risk: Trend summaries and content-alert templates may influence publishing decisions before the facts or platform rules are checked. <br>
Mitigation: Require human fact-checking, source review, and platform compliance review before using rankings or alerts for publication. <br>
Risk: Private sessions, cookies, or credentials would increase exposure if supplied to a live scraping workflow. <br>
Mitigation: Use only public data sources and do not provide private sessions, cookies, API keys, or account credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/e2e5g/hot-tracker) <br>
- [Objective hot-topic analysis framework](artifact/references/analysis-framework.md) <br>
- [Platform behavior rules and compliance checks](artifact/references/compliance-rules.md) <br>
- [Data format specification](artifact/references/data-format.md) <br>
- [Hot-topic Top10 output template](artifact/references/output-template.md) <br>
- [Timeliness analysis framework](artifact/references/timeliness-framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and rankings, with optional JSON-like structured fields and Python-assisted analysis outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is a neutral Top10 ranking with scores, platform coverage, confidence, reasons for popularity, noise notes, and representative sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
