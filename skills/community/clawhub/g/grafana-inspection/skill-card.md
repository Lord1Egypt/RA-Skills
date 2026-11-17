## Description:

This skill automates Grafana inspection by collecting API data, discovering dashboards, checking alerts and data sources, and producing JSON results and Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diluke1600](https://clawhub.ai/user/diluke1600)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Grafana dashboard health, active alerts, and data source status across specified or automatically discovered dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Grafana API tokens and optional login credentials may be stored in local configuration files.

Mitigation: Use a least-privilege Viewer-scoped token, avoid passing API keys on the command line, and keep configuration files out of source control and shared folders.

Risk: Automatic discovery can enumerate more dashboards than intended.

Mitigation: Set dashboard_uids explicitly, lower discover_limit, or disable auto_discover when broad dashboard enumeration is not desired.

Risk: Generated inspection reports may contain operational details about Grafana dashboards, alerts, and data sources.

Mitigation: Store generated reports in access-controlled local directories and avoid sharing or committing them unless reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diluke1600/skills/grafana-inspection)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands, plus timestamped JSON and Markdown inspection reports when run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local inspection_*.json and inspection_*.md files containing Grafana inspection results.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
