## Description: <br>
Queries and analyzes Kubernetes Pod stdout/stderr logs, CCE LogConfig-collected application logs, Huawei Cloud LTS log streams, and CCE audit logs for CCE workloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operations engineers and developers use this skill to retrieve, search, and summarize CCE workload logs, map LogConfig policies to LTS streams, inspect audit events, and identify abnormal log patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Huawei Cloud and Kubernetes credentials and may expose cluster state or secrets through log and configuration outputs. <br>
Mitigation: Use least-privilege credentials, keep AK/SK and Kubernetes credentials out of prompts and outputs, redact sensitive log values, and review generated files before sharing. <br>
Risk: LogConfig creation and deletion can change CCE log collection behavior. <br>
Mitigation: Use the documented preview-first flow and require explicit human approval before any confirm=true mutating action. <br>
Risk: The security scan reports insufficient guardrails for cloud-admin use. <br>
Mitigation: Install only in controlled cloud-administration environments and require human approval before actions that affect clusters, networks, node pools, workloads, or ECS state. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Risk Rules](references/risk-rules.md) <br>
- [Output Schema](references/output-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with structured fields and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include redacted log samples, query metadata, abnormality ratios, audit summaries, and preview payloads for LogConfig changes.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
