## Description: <br>
Grafana Inspector automates Grafana dashboard inspections with API data collection, dashboard discovery, health scoring, and JSON or Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diluke1600](https://clawhub.ai/user/diluke1600) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and platform operators use this skill to inspect Grafana dashboards, alerts, and data sources in batch and generate operational review reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Grafana credentials and may read them from local configuration. <br>
Mitigation: Use a least-privileged Viewer token, avoid storing long-lived secrets in config.json, and prefer an approved secrets workflow. <br>
Risk: One inspection script disables HTTPS certificate verification. <br>
Mitigation: Review or fix the TLS setting before installation; enable certificate verification or configure a trusted internal certificate authority. <br>
Risk: Auto-discovery and generated reports can expose internal monitoring details. <br>
Mitigation: Set the Grafana URL and dashboard scope explicitly, limit discovery, and keep reports out of shared or version-controlled directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diluke1600/grafana-inspector) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON inspection results, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports may include Grafana URLs, dashboard metadata, alert summaries, data source health, and operational findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
