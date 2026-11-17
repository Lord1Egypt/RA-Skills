## Description:

Creates Huawei Cloud IAM users and grants access by adding them to groups and attaching identity policies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and developers use this skill to create Huawei Cloud IAM users and authorize them through groups or identity policies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags weakened certificate verification for cloud connections.

Mitigation: Restore certificate verification before using production credentials.

Risk: The installer adds a telemetry executable whose downloaded implementation has not been reviewed.

Mitigation: Restore package-download verification, and review a pinned release and its reporting behavior before allowing access to cloud credentials; disable optional reports when they are not needed.

Risk: IAM changes can create users, groups, memberships, or policy attachments.

Mitigation: Preview the planned changes and require explicit confirmation before every write, including group creation.

## Reference(s):

- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Least-privilege IAM policies](artifact/references/iam-policies.md)
- [CLI installation and credential setup](artifact/references/cli-installation-guide.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain-text or JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include IAM identifiers, planned operations, and whether memberships or policy attachments already existed; dry-run previews are supported.]

## Skill Version(s):

1.0.10 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
