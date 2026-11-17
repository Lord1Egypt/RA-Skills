## Description:

Lists Huawei Cloud HSS protected hosts in a selected region through KooCLI, with an SDK fallback, server-side filters, pagination, and table, JSON, or name-only output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud security operators and developers use this skill to review HSS host inventory, protection and agent status, and enabled editions by region, including filtered checks for security patrols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a separate telemetry tool whose reporting behavior is not sufficiently explained.

Mitigation: Review the telemetry tool's payload, destination, and release verification before installing; prefer setting it up separately. If proceeding, use credentials limited to HSS host listing and clear test executable overrides. SKILL_QUALITY_REPORT=0 does not prevent installing or executing the wrapper.

## Reference(s):

- [ClawHub release](https://clawhub.ai/wlc-dev/skills/huawei-cloud-hss-list)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [CLI installation guide](references/cli-installation-guide.md)
- [Least-privilege IAM policies](references/iam-policies.md)
- [Data flow diagram](references/dataflow-diagram.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Aligned host table, JSON array, or newline-separated host names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only host inventory with optional region and server-side filters; output can be paginated across all matching hosts.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
