## Description:

Lists Huawei Cloud KMS master keys in a selected region and presents their aliases, identifiers, states, key details, and rotation status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and security engineers use it to inventory regional KMS keys and review their status for key audits or follow-on tasks that need a key ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release requires telemetry software whose remote payload and data handling could not be verified.

Mitigation: Review the telemetry software and its data handling before installation, or request a version that allows direct inventory execution without it.

Risk: Inventory completeness should be confirmed before using the results for an audit.

Mitigation: Independently check inventory completeness before relying on these results for an audit.

## Reference(s):

- [IAM read-only policy](artifact/references/iam-policies.md)
- [KooCLI installation and credentials guide](artifact/references/cli-installation-guide.md)
- [Data flow diagram](artifact/references/dataflow-diagram.md)
- [Verification method](artifact/references/verification-method.md)
- [Huawei Cloud KooCLI download guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [ClawHub release page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-kms-key-list)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Compact text list, full tabular inventory, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Region-scoped results with optional alias, key ID, and state filters; supports paginated inventory.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
