## Description:

Query Huawei Cloud CloudRobo quotas and resource pools, including workspace and domain capacity, filtered pool lists, and node-level details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect CloudRobo compute quotas and resource pools before planning training, evaluation, or inference workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connection guidance weakens protection against interception and falsified resource results when TLS certificate verification is disabled.

Mitigation: Set CLOUDROBO_VERIFY_SSL=true before connecting, confirm untrusted certificates are rejected, and repair certificate trust issues instead of bypassing verification. Restrict credentials to the documented read operations and keep traffic logging disabled.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cloudrobo-resource)
- [CLI installation and configuration](artifact/references/cli-installation-guide.md)
- [Credential and access guidance](artifact/references/iam-policies.md)
- [Resource API paths](artifact/references/api-paths.md)
- [Resource configuration reference](artifact/references/resource-config-catalog.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON quota and resource-pool results with command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only query results; filters and pagination are available.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
