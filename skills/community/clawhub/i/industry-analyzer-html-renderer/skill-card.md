## Description:

Renders a Chinese industry analysis report into a single-page, scrollable visual HTML report with charts, SVG diagrams, comparison tables, and timelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrxparley](https://clawhub.ai/user/zrxparley)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill as the final step in an industry-analysis pipeline to convert session data, four dimension reports, and a main Markdown report into a shareable HTML page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes an HTML report and updates session.json, which could overwrite existing local work.

Mitigation: Check output/{industry-slug}/industry-analysis-report.html and session.json before running, and preserve any work that should not be replaced.

## Reference(s):

- [行业分析 HTML 渲染 · 图表建议](references/chart-suggestions.md)
- [ClawHub Skill Page](https://clawhub.ai/zrxparley/skills/industry-analyzer-html-renderer)

## Skill Output:

**Output Type(s):** [Files, Code, Configuration]

**Output Format:** [HTML file with session status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes output/{industry-slug}/industry-analysis-report.html and updates session.json.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
