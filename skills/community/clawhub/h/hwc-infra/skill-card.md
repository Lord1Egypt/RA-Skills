## Description: <br>
Helps agents use Huawei Cloud KooCLI to query, audit, monitor, and, with confirmation, manage ECS, VPC, and RDS resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[5xuanwen](https://clawhub.ai/user/5xuanwen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and cloud administrators use this skill to inspect Huawei Cloud inventory, check ECS, VPC, and RDS health and security state, and prepare confirmed KooCLI commands for changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install a host-level CLI from a remote download source. <br>
Mitigation: Verify the KooCLI download source and integrity before installation, review the installer, and avoid elevated privileges unless necessary. <br>
Risk: The skill includes commands that can stop, restart, or delete cloud resources. <br>
Mitigation: Require the agent to show exact resource IDs and full commands, then wait for explicit confirmation before any mutating operation. <br>
Risk: Huawei Cloud credentials are needed for KooCLI configuration. <br>
Mitigation: Enter AK/SK credentials only through local KooCLI configuration and do not expose secrets in chat, logs, or command output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/5xuanwen/hwc-infra) <br>
- [KooCLI common commands](references/hcloud-queries.md) <br>
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html) <br>
- [Huawei Cloud KooCLI download source](https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline KooCLI shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only queries are the default; write or destructive commands require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
