## Description: <br>
Design Prometheus alerting rules and recording rules, analyze PromQL queries, set meaningful thresholds, reduce alert fatigue, and build multi-window multi-burn-rate SLO alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and observability teams use this skill to design or review Prometheus alerting rules, recording rules, Alertmanager routing, and SLO burn-rate alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated alert, routing, or deletion recommendations could disrupt production monitoring if applied without review. <br>
Mitigation: Manually review generated Prometheus and Alertmanager changes, test alert rules with promtool, and apply changes through normal change-control processes. <br>
Risk: Analysis against live Prometheus or Alertmanager systems may expose operational data or require credentials. <br>
Mitigation: Use read-only credentials for analysis and avoid sharing sensitive metric labels, endpoint details, or incident context beyond the intended reviewers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/prometheus-alert-designer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML configuration blocks and review findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PromQL expressions, Prometheus rule YAML, Alertmanager routing configuration, audit findings, and testing guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
