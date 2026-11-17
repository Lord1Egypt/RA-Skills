## Description:

Lists Huawei Cloud SFS file systems in a tenant region through KooCLI, with a Huawei Cloud SDK fallback and filtered table or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and storage operators use this skill to inventory file systems in a selected Huawei Cloud region and filter results for operational review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review flags a mismatch between the skill's credential-handling claims and its code, an unverified bundled installer source, and unvalidated live cloud behavior.

Mitigation: Use an existing KooCLI installation or Huawei's verified installation instructions, grant only SFS listing permissions, configure keys outside chat, and leave SFS_LIST_HCLOUD_BIN and SFS_LIST_HCLOUD_ARGS unset during normal use.

## Reference(s):

- [KooCLI installation and credential guide](references/cli-installation-guide.md)
- [Least-privilege IAM policy](references/iam-policies.md)
- [Verification method](references/verification-method.md)
- [Data flow diagram](references/dataflow-diagram.md)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [ClawHub release page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-sfs-list)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Aligned text table, JSON array, names-and-IDs list, or count]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Region-scoped SFS inventory with optional client-side filters and pagination.]

## Skill Version(s):

1.0.11 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
