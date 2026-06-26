## Description: <br>
Manage Hadoop clusters with HDFS operations, YARN job tuning, and distributed processing diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, data engineers, and Hadoop administrators use this skill to diagnose HDFS and YARN issues, tune distributed jobs, manage cluster storage, and troubleshoot Hadoop ecosystem failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HDFS and YARN commands can affect production cluster state or data when run with the user's current permissions. <br>
Mitigation: Confirm cluster state, exact HDFS paths, application IDs, and intended impact before executing destructive or administrative commands. <br>
Risk: Cluster notes may capture sensitive operational details if users paste credentials, keytabs, private hostnames, or production context. <br>
Mitigation: Keep credentials, keytabs, private hostnames, and sensitive production details out of local Hadoop memory files. <br>
Risk: Troubleshooting steps include commands that can delete data, kill applications, or change replication and queue behavior. <br>
Mitigation: Review proposed commands before execution, prefer reversible operations where possible, and use maintenance windows for disruptive actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/hadoop) <br>
- [Skill homepage](https://clawic.com/skills/hadoop) <br>
- [HDFS operations](hdfs.md) <br>
- [YARN operations](yarn.md) <br>
- [Troubleshooting](troubleshooting.md) <br>
- [Setup](setup.md) <br>
- [Memory template](memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local hdfs, yarn, and hadoop commands on Linux or macOS.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
