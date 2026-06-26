## Description: <br>
Analyzes GSC/GA4 data and live-site audit results to identify gaps between website goals and user behavior, then produces prioritized improvement plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morvanzhou](https://clawhub.ai/user/morvanzhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and marketing analytics teams use this skill to define website goals, collect or import GSC/GA4/Bing/PageSpeed data, audit the live site, and produce goal-aligned SEO, performance, funnel, and persona improvement reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles website analytics, Search Console data, OAuth/API credentials, and service-account keys. <br>
Mitigation: Use dedicated read-only credentials, keep the skill data directory private and out of git or synced folders, and delete or rotate stored keys and exports after the audit. <br>
Risk: Generated scripts and commands may access external analytics/search APIs or process sensitive exports. <br>
Mitigation: Review generated scripts and commands before running them, and run only the collection modes and data sources needed for the audit. <br>
Risk: Persona analysis can involve user demographics or behavioral data with consent and legal constraints. <br>
Mitigation: Avoid persona analysis unless the operator has the right consent and legal basis for the data being analyzed. <br>


## Reference(s): <br>
- [Data Collection Reference](references/data-collection-reference.md) <br>
- [Data Visualization Guide](references/data-visualization-guide.md) <br>
- [Key Metrics & Analysis Dimensions](references/metrics-glossary.md) <br>
- [SEO & GEO Optimization Checklist](references/SEO-GEO-Optimization-Checklist.md) <br>
- [Final Report Template](references/report-template.md) <br>
- [User Persona Analysis Reference](references/user-persona-analysis-reference.md) <br>
- [Website Reconnaissance Reference](references/website-reconnaissance-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance and reports with inline shell commands, generated Python analysis code, JSON audit outputs, and chart image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores raw exports, configuration, generated reports, scripts, logs, cache files, and charts under the skill data directory.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
