## Description:

Lists Huawei Cloud ECS instances in a selected region and exports the inventory to a local Excel workbook, table, or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and operations engineers use this skill to review and share a regional ECS inventory as a local report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled dependency setup helper disables download security checks, leaving downloaded packages without normal certificate verification.

Mitigation: Avoid the setup helper until its --trusted-host option is removed, or install dependencies from a certificate-verified package index in an isolated environment.

Risk: An ECS inventory report can expose cloud resource details if its local file is stored or shared openly.

Mitigation: Use read-only cloud credentials and save the report in a protected location.

## Reference(s):

- [Huawei Cloud KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [KooCLI, SDK, and Dependency Setup Guide](references/cli-installation-guide.md)
- [Least-Privilege ECS IAM Policy](references/iam-policies.md)
- [Verification Method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Files, Tables, JSON]

**Output Format:** [Excel (.xlsx), plain-text table, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Region selection, optional status and name filters, paging, and optional workbook path and summary row.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
