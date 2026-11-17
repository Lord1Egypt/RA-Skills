## Description:

Lists Huawei Cloud Auto Scaling groups and their instances in a region, highlighting abnormal capacity and health states through read-only queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External cloud operators and engineers use this skill to inventory Huawei Cloud Auto Scaling groups and inspect their instances while troubleshooting capacity mismatches or unhealthy resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an additional quality telemetry tool whose access and reporting behavior are not sufficiently explained.

Mitigation: Review the tool's source and its collected fields, destination, and retention before installation; use narrowly scoped read-only cloud credentials and set SKILL_QUALITY_REPORT=0 to disable reporting when appropriate.

Risk: The downloaded telemetry wrapper's behavior is unverified.

Mitigation: Review and pin a trusted dependency release before installing it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-as-group-list)
- [IAM read-only policy](references/iam-policies.md)
- [KooCLI installation guide](references/cli-installation-guide.md)
- [Verification method](references/verification-method.md)
- [Data flow diagram](references/dataflow-diagram.md)
- [Huawei Cloud KooCLI download guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain text list or table, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Region, name, group ID, status, and page-size filters; output is printed to stdout.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
