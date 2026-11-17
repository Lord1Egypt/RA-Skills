## Description:

Audits a Huawei Cloud VPC's network topology against configurable security rules and produces a report comparing the described access path with the discovered topology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud engineers and security teams use this read-only skill to compare a described access path with discovered Huawei Cloud resources, assess VPC network risks, and prepare a topology audit report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auditing a VPC exposes sensitive network configuration details to the skill.

Mitigation: Grant only the read-only IAM permissions needed for the relevant VPC, and keep secrets out of prompts and reports.

Risk: External quality reporting is enabled by default and may send masked audit inputs, outputs, errors, and stack traces.

Mitigation: Set SKILL_QUALITY_DISABLE=1 unless quality reporting is required.

Risk: The installation guide downloads an hcloud installer for optional CLI use.

Mitigation: Verify the installer before running it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-network-topology-audit)
- [Resource-skill mapping](references/resource-skill-mapping.md)
- [Audit rule authoring guide](references/rule-authoring-guide.md)
- [Read-only IAM permissions](references/iam-policies.md)
- [Huawei Cloud API documentation index](references/official-doc-index.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown audit report with a Mermaid topology diagram]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a described-versus-discovered topology comparison, rule-linked findings, and remediation guidance; an ASCII diagram is available as a fallback.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
