## Description:

Lists Huawei Cloud Bare Metal Server (BMS) instances by region through KooCLI, with an SDK fallback, filters, table, JSON, and name-list output, plus optional Markdown export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operations engineers use this skill to inspect Huawei Cloud Bare Metal Server inventories by region, filter servers, and export results for reconciliation or routine checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled KooCLI installation command downloads an installer whose source could not be verified.

Mitigation: Review the installer source before running it, obtain KooCLI through Huawei's official installation page, and verify the download.

Risk: Inventory exports may expose cloud infrastructure details, and the SDK fallback reads credentials from environment variables.

Mitigation: Use read-only credentials configured outside chat, protect exported inventory files, and keep credential environment variables private.

## Reference(s):

- [Huawei Cloud KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [KooCLI Installation and Credential Guide](references/cli-installation-guide.md)
- [Least-Privilege IAM Policy](references/iam-policies.md)
- [Data Flow Diagram](references/dataflow-diagram.md)
- [Verification Method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Console table or name list, JSON array, or Markdown inventory file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Region-scoped BMS inventory with optional filters and Markdown export.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
