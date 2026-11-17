## Description:

Helps agents answer questions and generate Markdown upgrade guides for Mingdao HAP private deployment upgrades, including version paths, deployment mode, architecture support, additional operations, commands, and validation notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuyanfeiwork](https://clawhub.ai/user/wuyanfeiwork)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, system administrators, and operations teams use this skill to plan Mingdao HAP private deployment upgrades and produce execution-ready upgrade guidance for standalone Docker Compose or Kubernetes cluster deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated upgrade guidance may include remote script one-liners for production hosts or Kubernetes control nodes.

Mitigation: Download scripts from trusted sources, verify integrity, inspect them before execution, and run them with the minimum required privileges.

Risk: Generated commands and runbooks may include placeholder or default credentials.

Mitigation: Replace defaults before use, avoid storing real credentials in shell history or shared documents, and use environment-specific secret handling.

Risk: Version and architecture compatibility can change after a guide is generated.

Mitigation: Verify the live Mingdao version table and linked upgrade pages before performing an upgrade.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuyanfeiwork/skills/hap-upgrade)
- [Mingdao private deployment documentation](https://docs-pd.mingdao.com)
- [Version release history](https://docs-pd.mingdao.com/version)
- [Site structure reference](references/site-structure.md)
- [Upgrade merge rules](references/merge-rules.md)
- [Upgrade command library](references/command-library.md)
- [Standalone upgrade guide template](assets/upgrade-guide-template-standalone.md)
- [Cluster upgrade guide template](assets/upgrade-guide-template-cluster.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or concise text with bash, YAML, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include upgrade path analysis, architecture compatibility findings, required pre-upgrade and post-upgrade operations, and verification notes.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
