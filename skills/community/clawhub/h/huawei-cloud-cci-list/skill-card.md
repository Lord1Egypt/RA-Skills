## Description:

Lists Huawei Cloud CCI namespaces, pods, and deployments in a selected region, with filtering and table, JSON, or compact name output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use this skill to inspect regional CCI inventory during routine operations and identify namespace, pod, or deployment names for follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required telemetry software does not document what it reports or where it sends the information.

Mitigation: Before installing, request documented reporting fields and destinations and use a separately approved, pinned dependency. Set SKILL_QUALITY_REPORT=0 to disable reporting when appropriate.

Risk: The downloaded wrapper was unavailable for inspection, so its data collection behavior cannot be confirmed or ruled out; disabling reporting does not remove its execution access.

Mitigation: Review the wrapper before use and use narrowly scoped, read-only cloud credentials.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wlc-dev/skills/huawei-cloud-cci-list)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [CLI installation and credential guide](references/cli-installation-guide.md)
- [Read-only IAM policies](references/iam-policies.md)
- [Verification method and API references](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Key-field text table, raw JSON objects, or compact namespace/name list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Region and resource scoped; supports namespace, name, label, and field filters.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
