## Description: <br>
Generates a Chinese daily news briefing by searching recent news across politics, finance, AI, technology, and consumer electronics, then saving a dated Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to produce a dated Chinese daily briefing covering global and China-focused news categories. It is suited for recurring news-report generation where the operator is comfortable with current-news web searches and local Markdown archives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on current-news web searches, so generated reports can reflect incomplete, stale, or low-quality search results. <br>
Mitigation: Review generated reports and source results before redistribution or decision-making. <br>
Risk: The skill saves dated Markdown reports locally, which can retain archived news content over time. <br>
Mitigation: Review scheduled-run setup before enabling it and delete old memory/daily_news_*.md files when report retention is not desired. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Dated Markdown news report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves reports to memory/daily_news_{YYYY-MM-DD}.md and may retain dated local archives.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
