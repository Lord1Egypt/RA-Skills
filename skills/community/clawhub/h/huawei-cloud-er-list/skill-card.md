## Description:

Lists Huawei Cloud Enterprise Routers, VPC attachments, route tables, and router details through read-only queries, with compact text, table, or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and developers use this skill to inspect Enterprise Router inventory, attachment and route table state, and network topology during operational checks. Its output can also provide router identifiers and state for follow-up queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates the release suspicious because it reports an unrelated CLI download and installation and telemetry tooling in a read-only inventory skill; the analysis was partial.

Mitigation: Avoid installation until the unrelated CLI and telemetry behavior are removed or independently reviewed, and the installer is pinned and verified through a trusted source.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-er-list)
- [Huawei Cloud KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [CLI installation and credentials](references/cli-installation-guide.md)
- [Least-privilege IAM policies](references/iam-policies.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Compact text, fixed-column table, or JSON resource inventory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports filtering and pagination; non-available routers and attachments are clearly separated from healthy resources.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
