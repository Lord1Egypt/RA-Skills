## Description:

Prometheus monitoring for scrape configuration, service discovery, recording rules, alert rules, and production deployment for infrastructure and application metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers, DevOps engineers, and SREs use this skill to set up Prometheus metrics collection, service discovery, recording rules, alert rules, and production monitoring practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes mutable npx install commands that can run remote code not included in the reviewed artifact.

Mitigation: Install from a pinned, reviewed release or manually copy reviewed artifact contents; avoid running mutable install commands with elevated privileges.

Risk: Prometheus templates contain scrape targets, alerting endpoints, and credential file paths that are placeholders or environment-specific.

Mitigation: Review and customize targets, Alertmanager settings, credential paths, thresholds, and retention settings before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/prometheus-devops)
- [Publisher profile](https://clawhub.ai/user/wpank)
- [Prometheus Community Helm Charts](https://prometheus-community.github.io/helm-charts)
- [Prometheus node_exporter](https://github.com/prometheus/node_exporter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Prometheus configuration, recording-rule, and alert-rule templates that require environment-specific review before deployment.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
