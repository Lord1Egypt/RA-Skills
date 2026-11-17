## Description:

Plans Huawei Cloud CCE container migrations by inventorying clusters, workloads, networking, storage, and configuration, then producing dependency maps, migration batches, risk assessments, rollback plans, and validation plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud migration engineers use this skill to assess Huawei Cloud CCE migration scope, map workload and infrastructure dependencies, and draft migration batches with rollback and validation plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packaged dispatcher behavior may perform live cloud or Kubernetes changes despite the skill's read-only migration-planning posture.

Mitigation: Review and remove or isolate mutation actions before installation, and run only with least-privilege read-only Huawei IAM and Kubernetes RBAC permissions.

Risk: Resource inventory can expose sensitive cluster data, including Secret metadata, project identifiers, tokens, certificates, or credentials.

Mitigation: Do not request Secret data; mask or omit project_id, AK/SK, tokens, and certificates from outputs, logs, files, and responses.

## Reference(s):

- [Workflow](references/workflow.md)
- [Risk Rules](references/risk-rules.md)
- [Output Schema](references/output-schema.md)
- [ClawHub skill page](https://clawhub.ai/pintudeyudi/skills/huawei-cloud-cce-container-migration-planner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Structured JSON migration plan with optional Markdown guidance and dispatcher command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes inventory, dependency matrix, migration batches, risks, rollback plan, and validation plan; sensitive IDs and credentials should be masked or omitted.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
