## Description:

Queries the total storage size of one Huawei Cloud OBS bucket or all buckets in an account and reports the result in bytes or a scaled human-readable value.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and engineers use this skill to measure storage for a specific OBS bucket or across an account for capacity reviews, cost estimates, and storage planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An all-buckets query covers account-wide bucket usage.

Mitigation: Confirm the requested scope before querying and use credentials restricted to the intended read-only bucket scope.

Risk: Inaccessible or failed buckets are skipped, so the reported aggregate can omit their contents.

Mitigation: Review warnings and confirm account-wide access before relying on an aggregate total.

Risk: Installing the CLI or obsutil involves downloading executable dependencies.

Mitigation: Download from the official Huawei Cloud source and verify the package against its current official checksum before installing.

Risk: Cloud credentials could grant broader access than the query needs.

Mitigation: Configure credentials locally and grant only the read-only permissions required for the intended bucket scope.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-obs-total-size)
- [Huawei Cloud CLI installation guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Least-privilege OBS IAM policy](artifact/references/iam-policies.md)
- [CLI installation and credential guidance](artifact/references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [A single size value in bytes by default, or scaled/human-readable text when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Warnings for skipped or inaccessible buckets are reported separately on stderr.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
