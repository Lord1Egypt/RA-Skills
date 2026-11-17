## Description:

Analyze Huawei Cloud WAF security event logs to summarize attack patterns and suggest protection rules for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to investigate Huawei Cloud WAF events, summarize attack activity, and review evidence-based protection rule suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command templates can mishandle hostile data in WAF event fields.

Mitigation: Have command escaping, protection examples, and temporary-file cleanup corrected before relying on generated recommendations.

Risk: Generated recommendations may weaken existing WAF protection.

Mitigation: Use dedicated read-only WAF credentials for analysis and review any suggested changes against the current policy before taking action.

Risk: Downloaded WAF logs may contain sensitive request details.

Mitigation: Protect downloaded logs and restrict access to the people who need them.

## Reference(s):

- [CLI Installation Guide](artifact/references/cli-installation-guide.md)
- [Rule Recommendation Guide](artifact/references/rule-recommendation-guide.md)
- [Verification Method](artifact/references/verification-method.md)
- [Data Flow Diagram](artifact/references/dataflow-diagram.md)
- [IAM Policies](artifact/references/iam-policies.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Structured Markdown report with tables and hcloud command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are based on the selected event scope and should be reviewed before use.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
