## Description:

Analyzes Apple Health export.zip files by streaming XML, extracting RHR, HRV, VO2 Max, sleep, steps, blood oxygen, and related metrics, then generating a personalized interactive HTML health report with Chart.js graphs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gloriaameng](https://clawhub.ai/user/gloriaameng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to process Apple Health exports and create personalized trend reports for fitness, sleep, cardiovascular, respiratory, and activity metrics. The reports can help users review trends and anomalies, but they should not be treated as medical diagnosis or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apple Health exports contain highly sensitive health information.

Mitigation: Only process exports the user is willing to expose to the agent environment, and delete export.zip, chart_data.json, and generated reports when analysis is complete.

Risk: Generated HTML reports may load Chart.js from a CDN and may display user-provided report text.

Mitigation: Open reports offline only after bundling Chart.js locally and verifying user-supplied text is escaped before rendering.

Risk: Health trend summaries and anomaly flags may be mistaken for clinical advice.

Mitigation: Present the output as trend analysis and advise users to consult a qualified clinician for medical concerns or abnormal readings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gloriaameng/skills/iwatch-health-data-analysis)
- [Publisher profile](https://clawhub.ai/user/gloriaameng)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, files, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON chart data, and an interactive HTML report file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes sensitive Apple Health exports in the agent environment; the generated report uses Chart.js and may load it from a CDN unless bundled locally.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
