## Description:

Lists Huawei Cloud Elastic IPs in a tenant region and returns a table, JSON array, names-only list, or Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect Huawei Cloud EIP inventory, filter results, and save an inventory report. It can also provide EIP IDs or bound-resource details for follow-on tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that environment values can redirect a subprocess from the intended read-only listing command, and the scan is incomplete because three path-like references were unresolved.

Mitigation: Review the reported command override and unresolved paths before use, and run with trusted environment values and read-only Huawei Cloud IAM permissions.

## Reference(s):

- [KooCLI installation guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Least-privilege IAM policy](artifact/references/iam-policies.md)
- [Verification method and API details](artifact/references/verification-method.md)
- [CLI installation and credential guide](artifact/references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Table, JSON array, compact names list, or Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports region and EIP filters; large results are paged.]

## Skill Version(s):

1.0.5 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
