## Description:

Queries Huawei Cloud Elastic Public IP resources and Cloud Eye bandwidth metrics, including usage rates, traffic, peak bandwidth, and averages over a chosen time range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to list and inspect Elastic Public IP resources and review Cloud Eye bandwidth utilization, traffic, and peak or average bandwidth for troubleshooting and capacity planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a reporting wrapper whose downloads, data handling, and upload-disable option are insufficiently explained or verified.

Mitigation: Before installation, ask the publisher to document uploaded data and destinations, provide pinned and verifiable downloads, and explain or remove the mandatory wrapper. Use narrowly scoped read-only cloud credentials and review installers before execution.

## Reference(s):

- [ClawHub release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-eip-query)
- [CLI installation guide](artifact/references/cli-installation-guide.md)
- [IAM permissions](artifact/references/iam-policies.md)
- [EIP metrics reference](artifact/references/eip-metrics-reference.md)
- [Data flow diagram](artifact/references/dataflow-diagram.md)
- [Verification method](artifact/references/verification-method.md)
- [Acceptance criteria](artifact/references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Concise summaries and Markdown tables of EIP details and monitoring metrics; JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports metric units, aggregation period, and time range when available.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
