## Description:

Analyzes Huawei Cloud CCE capacity trends, forecasts resource bottlenecks, simulates elasticity policies, and generates capacity reports with charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to plan Huawei Cloud CCE capacity, evaluate node and workload elasticity, and prepare reports that identify bottleneck and cost-optimization signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes tools beyond capacity forecasting that can expose Kubernetes credentials or secrets and delete or modify cluster resources.

Mitigation: Install only after narrowing the dispatcher to documented capacity actions, or run it with a tightly scoped read-only Huawei role that cannot generate kubeconfigs, list Secrets, or delete or mutate cluster resources.

Risk: Using broad production AK/SK credentials could increase the impact of unintended access or mutation paths.

Mitigation: Avoid production AK/SK credentials for the current package surface and use least-privilege credentials scoped to the analysis workflow.

Risk: Applying HPA or autoscaler changes can alter workload or node capacity behavior.

Mitigation: Use preview mode first, require explicit approval before any confirmed change, and document rollback and validation checks before applying changes.

## Reference(s):

- [Workflow](references/workflow.md)
- [Simulation Rules](references/simulation-rules.md)
- [Output Schema](references/output-schema.md)
- [Huawei Cloud Python SDK Documentation](https://doc.huihua.com/api/sdk/python.html)
- [Huawei Cloud API Explorer](https://support.huaweiicloud.com/apiexplorer/index.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JSON summaries, Markdown and HTML reports, SVG charts, and configuration previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write recurring history records and chart/report files when an output directory is provided.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
