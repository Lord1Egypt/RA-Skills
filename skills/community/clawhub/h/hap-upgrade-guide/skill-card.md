## Description: <br>
帮助明道云 HAP 私有部署用户评估跨版本升级、架构兼容性和附加操作，并生成单机或集群升级指南。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1447443432](https://clawhub.ai/user/1447443432) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to answer HAP private-deployment upgrade questions, check target-version architecture support, merge cross-version additional operations, and produce executable upgrade guidance for standalone or cluster deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated upgrade commands may affect production HAP private-deployment systems. <br>
Mitigation: Verify every command against current official documentation, confirm backups and rollback plans, and execute during an approved maintenance window. <br>
Risk: Generated guides or support artifacts could expose sensitive operational details if users include real secrets. <br>
Mitigation: Keep real passwords, tokens, and sensitive connection details out of generated guides, screenshots, tickets, and shell history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1447443432/hap-upgrade-guide) <br>
- [HAP private deployment version history](https://docs-pd.mingdao.com/version) <br>
- [HAP upgrade command library](artifact/references/command-library.md) <br>
- [HAP upgrade merge rules](artifact/references/merge-rules.md) <br>
- [Mingdao private deployment documentation site structure](artifact/references/site-structure.md) <br>
- [Standalone upgrade guide template](artifact/assets/upgrade-guide-template-standalone.md) <br>
- [Cluster upgrade guide template](artifact/assets/upgrade-guide-template-cluster.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or HTML upgrade guides with shell command and configuration code blocks, or concise advisory text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated guide filenames follow the HAP升级指南-v{current}-to-v{target}-{mode} naming pattern.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
