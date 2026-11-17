## Description:

Manage Hadoop clusters with HDFS operations, YARN job tuning, and distributed processing diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, data engineers, and Hadoop administrators use this skill to diagnose Hadoop cluster health, manage HDFS storage, tune YARN and MapReduce jobs, and troubleshoot distributed processing failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact Hadoop operations can delete data, kill workloads, alter permissions, change replication, trigger failover, decommission nodes, or affect service availability.

Mitigation: Require explicit user confirmation before delete, skipTrash, kill, failover, decommission, chmod, chown, or service-impacting commands, and check cluster state before acting.

Risk: The skill retains Hadoop cluster context locally, which may include sensitive cluster names, workflows, access notes, or operational details.

Mitigation: Avoid saving credentials or unnecessary sensitive access details, keep Kerberos and keytab handling separate, and review local notes for sensitive information.

Risk: Hadoop guidance can be wrong for a specific distribution, scheduler, security model, or cluster state.

Mitigation: Verify the Hadoop distribution, active scheduler, health reports, quotas, logs, and Kerberos or ACL context before applying tuning or repair steps.

## Reference(s):

- [ClawHub Hadoop Skill](https://clawhub.ai/ivangdavila/skills/hadoop)
- [Hadoop Skill Homepage](https://clawic.com/skills/hadoop)
- [HDFS Operations](hdfs.md)
- [YARN Operations](yarn.md)
- [Troubleshooting](troubleshooting.md)
- [Setup](setup.md)
- [Memory Template](memory-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local Hadoop CLI commands and local memory updates for cluster context.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
