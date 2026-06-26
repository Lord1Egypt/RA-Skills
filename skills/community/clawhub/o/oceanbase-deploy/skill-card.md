## Description: <br>
Overview skill for OceanBase deployment and operations using obd. Routes to specialized skills for cluster management, tenant management, seekdb, and testing. Use as a starting point when the user's intent is not yet clear, or for general OceanBase obd questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oceanbase](https://clawhub.ai/user/oceanbase) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database operators, and platform engineers use this skill to plan OceanBase OBD deployments and generate operational guidance for cluster lifecycle management, tenant management, seekdb HA, monitoring, backup and restore, and benchmark workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated commands can perform high-impact database and cluster actions such as tenant drop, restore, component deletion, cluster destruction, failover, and benchmark runs. <br>
Mitigation: Require explicit user confirmation before executing these actions, review command targets and parameters, and test workflows on non-production clusters first. <br>
Risk: Operational commands may require credentials for OceanBase, OCP, Prometheus, SSH, or backup storage. <br>
Mitigation: Avoid pasting real passwords into chat or shell history; prefer secure secret handling and redact credentials from generated examples. <br>
Risk: Incorrect OBD deployment or HA guidance can cause data loss, downtime, or invalid standby topology. <br>
Mitigation: Validate cluster state, component availability, backup paths, and primary-standby requirements before applying changes. <br>


## Reference(s): <br>
- [OceanBase Deploy ClawHub Page](https://clawhub.ai/oceanbase/oceanbase-deploy) <br>
- [OceanBase OBD Quick Start](https://www.oceanbase.com/docs/common-obd-cn-1000000005246289) <br>
- [OceanBase Community Mirror](https://mirrors.oceanbase.com/community/stable/el/) <br>
- [Config File Deployment](cluster-management/references/config-deployment.md) <br>
- [OCP CE Deployment and Takeover](cluster-management/references/ocp-ce.md) <br>
- [Monitoring Setup](cluster-management/references/monitoring.md) <br>
- [seekdb Install Modes](seekdb/references/install-modes.md) <br>
- [seekdb HA Operations](seekdb/references/ha-operations.md) <br>
- [Backup and Restore](tenant-management/references/backup-restore.md) <br>
- [Test Command Details](testing-and-benchmark/references/test-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should be treated as proposals and reviewed before execution.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
