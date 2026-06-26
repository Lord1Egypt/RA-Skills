## Description: <br>
Query Prometheus metrics, alerts, and cluster status using PromQL with options for direct URL or Kubernetes port-forward access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peintune](https://clawhub.ai/user/peintune) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to query Prometheus for alerts, cluster health, nginx metrics, and custom PromQL results from a chosen Prometheus endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Metric labels and alert annotations may expose sensitive infrastructure details. <br>
Mitigation: Only query trusted Prometheus endpoints and review outputs before sharing them outside the intended operational context. <br>
Risk: A kubectl port-forward can connect to an unintended namespace or service if copied without checking the target. <br>
Mitigation: Verify the namespace and service name before running the port-forward command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peintune/prometheus-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text metric results and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prometheus endpoint, query, time range, step, and timeout are user-selected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
