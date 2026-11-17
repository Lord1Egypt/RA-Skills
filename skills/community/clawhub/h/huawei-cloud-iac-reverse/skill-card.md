## Description:

Reverse-engineer existing Huawei Cloud resources into deployable Terraform IaC code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to inventory existing Huawei Cloud resources, generate Terraform HCL for top-level infrastructure, validate the configuration, and compare generated resources against the original cloud inventory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote installer commands may execute unverified code in an environment that also has Huawei Cloud credentials.

Mitigation: Review installer contents before execution and install KooCLI through a trusted Huawei Cloud channel instead of piping a download directly to bash.

Risk: Cloud inventory, Terraform plans, and generated configuration can expose sensitive infrastructure metadata.

Mitigation: Store generated inventory and plan files in a controlled location, restrict sharing, and remove or redact sensitive details before publication.

Risk: Terraform apply can create or modify resources if run after generation.

Mitigation: Use the skill for discovery, generation, validation, and plan review; run terraform apply only after explicit human approval.

Risk: Over-privileged Huawei Cloud credentials increase blast radius during discovery and validation.

Mitigation: Use a least-privilege read-only key limited to required list, get, and show permissions.

## Reference(s):

- [README](README.md)
- [IAM Policies](references/iam-policies.md)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Data Flow Diagram](references/dataflow-diagram.md)
- [ClawHub Release Page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-iac-reverse)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and Terraform HCL file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local inventory, validation, plan comparison, and gap-analysis outputs; terraform apply is reserved for explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
