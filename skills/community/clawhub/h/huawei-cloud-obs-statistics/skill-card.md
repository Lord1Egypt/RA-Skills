## Description:

Produces read-only Huawei Cloud OBS summaries of bucket and object counts, estimated capacity, and storage-class and region distributions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inventory OBS buckets and summarize object counts, estimated capacity, storage classes, and regions across an account, bucket, or key prefix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised scan limits and pagination defects can produce incomplete statistics that appear complete.

Mitigation: Do not rely on --max-objects or treat reports as complete until collection limits and pagination are corrected; validate results before using them.

Risk: The CLI and SDK execution paths may use different accounts or access more buckets than intended.

Mitigation: Use dedicated read-only credentials restricted to the intended buckets, and confirm which account both paths use.

Risk: CLI downloads and external dependency contents are unverified, and live cloud behavior has not been validated.

Mitigation: Verify CLI downloads before installation and review the skill before use.

## Reference(s):

- [ClawHub release](https://clawhub.ai/wlc-dev/skills/huawei-cloud-obs-statistics)
- [Least-privilege IAM policy](references/iam-policies.md)
- [CLI installation guide](references/cli-installation-guide.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Aligned text table, JSON summary, or Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Aggregated counts and distributions; capacity is an estimate based on object sizes, and collection may be incomplete.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
