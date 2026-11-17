## Description:

Guides Huawei Cloud MRS HDFS performance diagnosis through alarm checks, quick checks, and local log analysis with trend charts and a root-cause summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

HDFS operators and engineers use this skill to investigate slow reads or writes, RPC latency, and NameNode alarms by correlating cluster checks with local operational logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HDFS operational and audit logs, including generated reports, may expose usernames, paths, and cluster details.

Mitigation: Limit access to the logs and keep reports local unless their contents have been reviewed before sharing.

Risk: Restarts, balancing, or configuration changes proposed during diagnosis can disrupt cluster operations.

Mitigation: Require human approval and an operational review before carrying out repair steps.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-mrs-hdfs-performance-issue-analysis)
- [ClawHub publisher profile](https://clawhub.ai/user/huaweicloudskill)
- [IAM permissions reference](references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Guidance]

**Output Format:** [Markdown guidance, local HTML trend charts, and a text analysis summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The analyzer writes 10 interactive HTML charts and analysis_summary.txt to the logs' trends directory for a selected time window.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
