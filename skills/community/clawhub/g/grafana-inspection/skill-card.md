## Description: <br>
This skill inspects Grafana dashboards through the Grafana API, discovers dashboards, checks active alerts and datasource health, and writes JSON and Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diluke1600](https://clawhub.ai/user/diluke1600) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to run local Grafana inspections, summarize dashboard coverage, alert state, datasource health, and export the findings for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Grafana API key and connects to a configured Grafana URL. <br>
Mitigation: Use a dedicated Viewer-scoped API key, verify the Grafana URL before running the skill, and avoid storing credentials in shared configuration files. <br>
Risk: Generated inspection reports can reveal internal monitoring details, dashboard names, alert states, datasource names, and service health information. <br>
Mitigation: Keep generated JSON and Markdown reports private, review them before sharing, and remove sensitive operational details when reports leave the trusted environment. <br>
Risk: The release documentation describes hybrid screenshot inspection, while the security evidence says to expect API inspection only unless browser screenshot support is added. <br>
Mitigation: Treat screenshot output as unavailable unless the publisher adds and documents real browser screenshot support; rely on the generated API inspection reports for current behavior. <br>


## Reference(s): <br>
- [Grafana Insepction on ClawHub](https://clawhub.ai/diluke1600/grafana-inspection) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON and Markdown reports, plus console status output and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include timestamped inspection JSON, timestamped Markdown reports, dashboard summaries, alert counts, datasource health, and an overall health score.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
