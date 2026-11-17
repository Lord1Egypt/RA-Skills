## Description:

Generates consolidated Huawei Cloud CCE operations reports that combine daily inspection, capacity trends, availability risk, cost optimization, and on-call context into Markdown, HTML, JSON, and chart outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to generate weekly, monthly, SLA, capacity, or stability reports for Huawei Cloud CCE clusters by aggregating inspection, capacity, availability, cost, and on-call signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill claims read-only reporting but ships callable code for Secret-data access and live cluster changes.

Mitigation: Review before installation, require a report-only dispatcher with an enforced allowlist, and remove undeclared mutation and Secret-data actions before normal use.

Risk: Broad Huawei Cloud or Kubernetes administrator credentials could expose more privileges than the reporting workflow needs.

Mitigation: Test only in an isolated environment with least-privilege, read-only cloud and Kubernetes credentials.

Risk: Raw output and on-call inputs can contain sensitive operational context.

Mitigation: Avoid include_raw unless audit traceability is required, restrict on-call input paths to trusted files, and review or redact persisted report artifacts.

Risk: The security guidance calls out TLS verification, temporary credential handling, and unpinned dependencies as issues to fix.

Mitigation: Fix TLS verification and temporary credential handling, and pin dependencies before production deployment.

## Reference(s):

- [Workflow](references/workflow.md)
- [Output Schema](references/output-schema.md)
- [ClawHub skill page](https://clawhub.ai/pintudeyudi/skills/huawei-cloud-cce-ops-report-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, JSON, and optional SVG chart files, with command guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can persist report artifacts to output_dir and can include raw source payloads when include_raw=true.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
