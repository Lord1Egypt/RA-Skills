## Description:

Inspect Huawei Cloud BCS instances, channels, members, quotas, alerts, and metrics, and manage resources, certificates, and invitations through guided operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect Huawei Cloud Blockchain Service and manage BCS resources, union membership, certificates, and SDK configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence rates the skill suspicious with medium confidence because setup installs a separate CLI without a separate approval step, and its telemetry and release verification are unclear; the scan was also partial.

Mitigation: Follow the security guidance: avoid installation until the CLI is optional, its telemetry destination and data are explained, and its release is pinned and authenticated. Review the unresolved local-path file to complete the assessment.

Risk: Write operations can incur charges or cause irreversible resource and data changes.

Mitigation: Review the operation preview and cost or data impact, and get explicit approval naming the target before running a write with --confirm.

Risk: Downloaded certificates and SDK configuration contain private key material.

Mitigation: Keep downloaded files private, store them securely, and do not commit or share them. The skill documents owner-only file permissions.

## Reference(s):

- [ClawHub Release Page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-bcs-manage)
- [Workflow](references/workflow.md)
- [IAM Policies](references/iam-policies.md)
- [Body File Schemas](references/body-file-schemas.md)
- [CLI Installation Guide](references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration files]

**Output Format:** [Text tables, JSON payloads, and optional certificate or Fabric SDK configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only reports, write-operation previews and results, and optional sensitive certificate or SDK configuration downloads.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
