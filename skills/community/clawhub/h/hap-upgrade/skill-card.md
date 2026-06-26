## Description: <br>
明道云 HAP 私有部署版本升级专属 skill，用于 HAP 私有部署升级咨询、跨版本附加操作合并、架构兼容性校验，以及单机或集群升级指南生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuyanfeiwork](https://clawhub.ai/user/wuyanfeiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to plan and document Mingdao HAP private-deployment upgrades. It helps gather required upgrade inputs, verify architecture support against official documentation, merge cross-version additional operations, and produce executable Markdown runbooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated upgrade runbooks may include production-impacting commands for HAP private deployments. <br>
Mitigation: Confirm all generated steps against official Mingdao documentation, complete backups, and execute during an approved maintenance window. <br>
Risk: The skill may surface remote script commands as part of upgrade guidance. <br>
Mitigation: Download, inspect, and verify remote scripts before execution, especially in production or regulated environments. <br>
Risk: Upgrade planning may require sensitive operational details. <br>
Mitigation: Avoid pasting real passwords or secrets into chat; use placeholders and apply credentials only in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/wuyanfeiwork/hap-upgrade) <br>
- [Mingdao private deployment documentation](https://docs-pd.mingdao.com) <br>
- [Mingdao HAP version history](https://docs-pd.mingdao.com/version) <br>
- [Command library](references/command-library.md) <br>
- [Merge rules](references/merge-rules.md) <br>
- [Site structure](references/site-structure.md) <br>
- [Standalone upgrade guide template](assets/upgrade-guide-template-standalone.md) <br>
- [Cluster upgrade guide template](assets/upgrade-guide-template-cluster.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces consultation answers or executable upgrade-guide Markdown; generated operations content should be verified against official Mingdao documentation before use.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
