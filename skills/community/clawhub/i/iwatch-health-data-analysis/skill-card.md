## Description: <br>
Analyzes Apple Health export.zip data to extract key Apple Watch health metrics and generate a personalized interactive HTML health report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gloriaameng](https://clawhub.ai/user/gloriaameng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent users use this skill to analyze Apple Health exports, compare heart, sleep, activity, blood oxygen, and body metrics against personalized baselines, and produce an interactive local health report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes Apple Health exports that contain sensitive health data. <br>
Mitigation: Run it in a private workspace, avoid sharing the export.zip beyond the active analysis, and delete the export and generated reports when finished. <br>
Risk: The workflow examples write derived chart data to the default /tmp path. <br>
Mitigation: Choose a private output path for chart_data.json and the HTML report when running the scripts. <br>
Risk: The generated HTML report loads Chart.js from a public CDN when opened online. <br>
Mitigation: Open the report only when that network behavior is acceptable, or bundle Chart.js locally before viewing. <br>
Risk: Health trend summaries may be mistaken for medical diagnosis. <br>
Mitigation: Treat the report as informational guidance and consult a qualified clinician for medical decisions or concerning results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gloriaameng/iwatch-health-data-analysis) <br>
- [Chart.js CDN used by generated report](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown instructions with Python commands, JSON chart data, and an interactive HTML report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Parses Apple Health export.zip into chart_data.json and generates a local HTML report with Chart.js visualizations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
