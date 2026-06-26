## Description: <br>
Enhanced monitoring with Prometheus, Grafana, Loki, alerting rules, dashboard templates, and SLO/SLI tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to draft monitoring configurations, alerting rules, dashboard templates, PromQL and LogQL queries, and SLO/SLI tracking guidance for observability stacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example credentials, service keys, and webhook placeholders may be copied into real alerting configurations. <br>
Mitigation: Replace all example secrets with secret-manager or environment-variable references and avoid committing real tokens. <br>
Risk: The Loki example disables authentication and could expose logs if deployed unchanged. <br>
Mitigation: Do not deploy Loki with auth disabled unless it is isolated and otherwise protected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/monitoring-plus) <br>
- [Publisher profile](https://clawhub.ai/user/534422530) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with YAML, JSON, PromQL, and LogQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces documentation and examples for monitoring setup; it does not execute monitoring tools directly.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
