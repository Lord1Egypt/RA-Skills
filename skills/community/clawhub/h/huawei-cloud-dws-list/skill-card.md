## Description:

Lists Huawei Cloud Data Warehouse Service clusters in a selected region and returns a table, JSON array, or cluster-name list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use the skill to inspect DWS cluster inventory, status, and connection details in a Huawei Cloud region. It can also provide cluster names or JSON data for follow-on workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command overrides bypass the advertised read-only safeguards.

Mitigation: Prefer a corrected release that constrains command overrides, rejects unsupported regions, and documents credential handling accurately; use dedicated read-only credentials and a trusted CLI in a controlled environment.

Risk: Live cloud behavior and downloaded installer or dependency contents were not verified.

Mitigation: Use a trusted CLI in a controlled environment and keep access limited to dedicated read-only credentials.

## Reference(s):

- [Huawei Cloud KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [API Verification Method](artifact/references/verification-method.md)
- [Read-Only IAM Policies](artifact/references/iam-policies.md)
- [CLI Installation and Credential Guide](artifact/references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Cluster inventory table, JSON array, or cluster-name list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional region and enterprise project selection, client-side filters, and pagination]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
