## Description:

Analyzes website goals, user journeys, GSC and GA4 data, and live-site audit evidence to produce actionable, goal-aligned improvement plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morvanzhou](https://clawhub.ai/user/morvanzhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and marketing analysts use this skill to diagnose website performance, SEO, GEO, analytics, conversion, and user journey gaps. It helps collect or process GSC, GA4, Bing Webmaster, PageSpeed, browser audit, and source-code evidence into prioritized improvement reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access website analytics, search console data, and local credential files.

Mitigation: Use least-privilege read-only accounts, restrict data directory permissions, and store service account keys only in the configured local configs directory.

Risk: Live-site and sitemap audits can fetch many URLs from the configured target site.

Mitigation: Review the configured SITE_URL and sitemap scope before running audit scripts, and limit page counts when auditing unfamiliar sites.

Risk: Dependency drift can change script behavior over time.

Mitigation: Prefer pinned dependencies or a lockfile before production use.

## Reference(s):

- [Skill release page](https://clawhub.ai/morvanzhou/skills/improve-skill-with-best-practices)
- [Website Reconnaissance Reference](references/website-reconnaissance-reference.md)
- [Data Collection Reference](references/data-collection-reference.md)
- [SEO & GEO Optimization Checklist](references/SEO-GEO-Optimization-Checklist.md)
- [Data Visualization Guide](references/data-visualization-guide.md)
- [Key Metrics & Analysis Dimensions](references/metrics-glossary.md)
- [User Persona Analysis Reference](references/user-persona-analysis-reference.md)
- [Final Report Template](references/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON audit outputs, generated chart files, Python analysis scripts, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores runtime data, credentials, raw API exports, analysis outputs, charts, logs, cache, and temporary screenshots under a local .skills-data directory.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
