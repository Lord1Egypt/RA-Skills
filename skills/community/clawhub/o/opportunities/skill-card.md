## Description:

opportunities helps an agent evaluate patent opportunities for a focused technology direction or technical proposal by using PatSnap/Zhihuiya patent search and analysis tools to produce HTML reports, structured data, CSV evidence, and investment or R&D recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, patent analysts, R&D teams, and investment evaluators use this skill to assess whether a narrowly scoped technology direction is worth researching or investing in. The skill generates patent trend analysis, subfield comparisons, evidence mappings, representative patent lists, and a final recommendation grounded in patent-data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may execute embedded or third-party JavaScript when opened.

Mitigation: Treat generated reports as active web pages, sanitize untrusted patent data before opening, and prefer a revised version that escapes dynamic fields and vendors chart assets locally.

Risk: The skill writes persistent local report files that may include patent-search results and analysis artifacts.

Mitigation: Review generated files before sharing, store outputs only in approved locations, and delete reports that contain sensitive or unnecessary search results.

Risk: The workflow depends on PatSnap/Zhihuiya MCP searches and may expose query terms to configured patent-search services.

Mitigation: Use only approved MCP credentials and avoid submitting confidential technology details unless the connected service is authorized for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/opportunities)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)
- [ECharts 5.4.3 CDN](https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js)
- [Example input](references/examples/example_input.md)
- [Example output structure](references/examples/example_output_structure.md)
- [HTML report generation prompt](references/prompts/html_report_generation_prompt.md)
- [Quality check prompt](references/prompts/quality_check_prompt.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance, Files]

**Output Format:** [HTML, JSON, CSV, and Markdown report files with a short final Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected release output is a 10-file patent opportunity report, including multi-page HTML, intermediate JSON, patent and evidence CSV files, README, and quality-check documentation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
