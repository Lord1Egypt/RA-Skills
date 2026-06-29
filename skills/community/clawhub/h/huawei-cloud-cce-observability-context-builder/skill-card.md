## Description: <br>
Collects and consolidates Huawei Cloud CCE alarms, metrics, logs, and events into an observability context package for diagnosis handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and SREs use this skill to gather Huawei Cloud CCE observability signals across a selected time window and produce structured context for incident diagnosis or hand-off. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package is presented as read-only observability, but server security evidence reports broad cloud and Kubernetes admin surfaces plus sensitive credential-handling paths. <br>
Mitigation: Restrict execution to the listed observability actions and use least-privilege read-only IAM and Kubernetes credentials. <br>
Risk: The skill can handle sensitive cluster material, logs, reports, and credentials. <br>
Mitigation: Run it in an isolated workspace, avoid account-wide admin AK/SK, do not enable raw secret or kubeconfig outputs, and sanitize log excerpts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pintudeyudi/huawei-cloud-cce-observability-context-builder) <br>
- [Workflow](references/workflow.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [Risk Rules](references/risk-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON context-package structure and shell command proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize alarms, events, metrics, logs, timeline gaps, and recommended next diagnostic skill.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
