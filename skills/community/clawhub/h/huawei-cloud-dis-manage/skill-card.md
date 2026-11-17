## Description:

Manages Huawei Cloud DIS streams, transfer tasks, monitoring, consumer checkpoints, data verification, policies, and tags through the hcloud CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud developers and operators use the skill to inspect and manage Huawei Cloud DIS streams, transfer tasks, consumers, and access policies. It can prepare operational commands and produce inventory, monitoring, and data verification reports, with confirmation required for high-risk changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports supply chain and privacy concerns related to unrelated quality telemetry tooling used during DIS operations; the scan is partial and some local references were unresolved.

Mitigation: Review the telemetry tool's source and data handling, and resolve the flagged references before installation or use. The skill documents SKILL_QUALITY_REPORT=0 to disable telemetry reporting.

Risk: DIS operations can change or delete streams, transfer tasks, consumer apps, checkpoints, and access policies, and data verification can upload records.

Mitigation: Confirm each high-risk operation with the user, verify the target and region, and use synthetic records for data-path checks.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-dis-manage)
- [Publisher profile](https://clawhub.ai/user/huaweicloudskill)
- [DIS operation catalog](artifact/references/dis-operation-catalog.md)
- [CLI installation guide](artifact/references/cli-installation-guide.md)
- [IAM policies](artifact/references/iam-policies.md)
- [Verification method](artifact/references/verification-method.md)
- [Acceptance criteria](artifact/references/acceptance-criteria.md)
- [Data flow diagram](artifact/references/dataflow-diagram.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stream inventories, monitoring summaries, verification results, and proposed actions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
