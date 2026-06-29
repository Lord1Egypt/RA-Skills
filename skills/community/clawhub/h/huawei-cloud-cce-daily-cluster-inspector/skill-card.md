## Description: <br>
Huawei Cloud CCE Daily Cluster Inspector runs read-only health inspections for Huawei Cloud CCE clusters, starting with quick checks and escalating to deeper diagnostics when anomalies are found. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations engineers and cloud platform teams use this skill for daily or periodic Huawei Cloud CCE cluster health checks, heartbeat summaries, post-change validation, and first-pass triage before deeper diagnosis or remediation handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary says the skill is presented as a read-only daily CCE inspector, but its bundled dispatcher exposes cluster credentials, secret data, and multiple cloud or Kubernetes mutation actions. <br>
Mitigation: Treat it as a broad Huawei Cloud CCE administration toolkit, review and disable mutating actions before production use, and execute only the read-only inspection workflow. <br>
Risk: The skill requires sensitive Huawei Cloud credentials and may handle cluster access material. <br>
Mitigation: Use least-privilege IAM credentials, avoid passing AK/SK values as parameters, do not expose credentials in commands or reports, and avoid subagent mode with real secrets. <br>


## Reference(s): <br>
- [Workflow](artifact/references/workflow.md) <br>
- [Risk Rules](artifact/references/risk-rules.md) <br>
- [Output Schema](artifact/references/output-schema.md) <br>
- [Publisher Profile](https://clawhub.ai/user/pintudeyudi) <br>
- [Skill Page](https://clawhub.ai/pintudeyudi/huawei-cloud-cce-daily-cluster-inspector) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown or JSON inspection summaries with risk classifications, recommended follow-ups, and optional report file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should avoid secrets such as AK/SK values, tokens, certificates, and full kubeconfig content.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
