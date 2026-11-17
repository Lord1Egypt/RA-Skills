## Description:

Manage Huawei Cloud Elastic Cloud Server instances across creation, queries, power state changes, operating system changes, resizing, deletion, and linked-resource lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect Huawei Cloud ECS instances and manage their lifecycle through KooCLI or the Huawei Cloud SDK. It requires confirmation before state-changing operations that can affect service availability, data, or cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic quality reporting may disclose sensitive server information, and cloud credentials may be handled unsafely.

Mitigation: Set SKILL_QUALITY_DISABLE=1 unless the data transfer is deliberately approved. If reporting is needed, require reliable secret filtering, a fixed HTTPS destination, verified TLS, and separate restricted credentials.

Risk: ECS mutations can change availability, remove data, or incur charges.

Mitigation: Use task-scoped cloud permissions and review the exact command and parameters; require explicit user confirmation before each mutation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ecs-lifecycle)
- [KooCLI installation and usage guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [CLI installation guide](references/cli-installation-guide.md)
- [IAM permissions](references/iam-policies.md)
- [Lifecycle change operations](references/lifecycle-change-operations.md)
- [Linked resource queries](references/linked-resource-queries.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with explanatory text and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide read-only queries or proposed state-changing commands; state changes require explicit user confirmation.]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
