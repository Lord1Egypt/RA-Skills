## Description:

Lists Huawei Cloud ECS instances in a selected region and exports the inventory as a local Markdown report, table, or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and operations engineers use this skill to review regional ECS inventory and prepare a local report for operations patrols or documentation.

### Deployment Geography for Use:

Global, wherever Huawei Cloud ECS is available.

## Known Risks and Mitigations:

Risk: The supplied environment helper installs SDK dependencies using package mirrors with trusted-host settings, which can weaken download verification.

Mitigation: Install required SDK packages through a certificate-verified package source instead of using the supplied environment helper.

Risk: The quality reporting program may send usage data, and its data handling could not be verified.

Mitigation: Set SKILL_QUALITY_REPORT=0 and skip the quality CLI installers unless the program and its reporting policy have been separately reviewed.

Risk: Exported ECS inventory can expose cloud resource details.

Mitigation: Protect generated report files and use credentials limited to ECS listing permissions.

## Reference(s):

- [Huawei Cloud ECS Export Markdown on ClawHub](https://clawhub.ai/wlc-dev/skills/huawei-cloud-ecs-export-markdown)
- [Huawei Cloud KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Least-Privilege IAM Policy](artifact/references/iam-policies.md)
- [CLI Installation and Credential Guide](artifact/references/cli-installation-guide.md)
- [Data Flow Diagram](artifact/references/dataflow-diagram.md)
- [Verification Method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, JSON, Files]

**Output Format:** [Local Markdown report, terminal table, or JSON instance data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Region-aware inventory with optional status and name filters and pagination; Markdown reports are written locally.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
