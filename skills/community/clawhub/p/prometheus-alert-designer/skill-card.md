## Description:

Design Prometheus alerting rules and recording rules - analyze PromQL queries, set meaningful thresholds, reduce alert fatigue, and build multi-window multi-burn-rate SLO alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and observability teams use this skill to design or review Prometheus alerting rules, recording rules, SLO burn-rate alerts, and Alertmanager routing that reduce alert fatigue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect alert thresholds, routing rules, or paging severity can cause noisy alerts or missed incidents.

Mitigation: Review generated alert and routing rules before deployment, validate PromQL and YAML with Prometheus tooling, and confirm receiver targets and escalation paths.

Risk: Providing broad monitoring access can expose more operational data than the alert design task requires.

Mitigation: Provide only the Prometheus, Grafana, or Alertmanager access needed for the specific review or design task.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/skills/prometheus-alert-designer)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with YAML and PromQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recording rules, alert rules, Alertmanager routing guidance, audit findings, and testing plans.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
