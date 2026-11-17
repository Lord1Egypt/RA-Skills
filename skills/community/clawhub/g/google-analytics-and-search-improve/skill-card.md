## Description:

Analyzes website goals, Google Search Console and GA4 data, and live-site audits to produce goal-aligned SEO, performance, UX, and conversion improvement plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morvanzhou](https://clawhub.ai/user/morvanzhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and growth teams use this skill to diagnose website search, analytics, performance, technical SEO, GEO readiness, and conversion issues. It helps turn confirmed site goals and collected data into prioritized improvement reports and implementation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Site-audit scripts can be directed to request internal network URLs through user-supplied URLs, sitemaps, or redirects.

Mitigation: Use the skill only on sites you control or trust, avoid untrusted sitemaps, and add URL validation before using it in environments with access to private networks or cloud metadata services.

Risk: Analytics and webmaster data collection uses service account files and API keys stored under the skill data directory.

Mitigation: Use read-only analytics credentials, restrict permissions on .skills-data, and remove or rotate keys when the work is complete.

## Reference(s):

- [Data Collection Reference](references/data-collection-reference.md)
- [Data Visualization Guide](references/data-visualization-guide.md)
- [Key Metrics and Analysis Dimensions](references/metrics-glossary.md)
- [SEO and GEO Optimization Checklist](references/SEO-GEO-Optimization-Checklist.md)
- [Website Reconnaissance Reference](references/website-reconnaissance-reference.md)
- [Final Report Template](references/report-template.md)
- [User Persona Analysis Reference](references/user-persona-analysis-reference.md)
- [Google Search Console](https://search.google.com/search-console/)
- [Google Analytics](https://analytics.google.com/)
- [Google Structured Data Documentation](https://developers.google.com/search/docs/appearance/structured-data)
- [Schema.org](https://schema.org/)
- [IndexNow Protocol](https://www.indexnow.org/)
- [llms.txt Standard Proposal](https://llmstxt.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON audit data, PNG charts, Python scripts, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes runtime data, raw inputs, analysis reports, charts, cache, configuration, logs, and temporary files under .skills-data/google-analytics-and-search-improve/.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
