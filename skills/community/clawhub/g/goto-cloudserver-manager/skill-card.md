## Description:

Automates multi-cloud server operations for Alibaba Cloud, Tencent Cloud, and Huawei Cloud, including database installation, schema creation, monitoring checks, and health reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feixuelingcloud](https://clawhub.ai/user/feixuelingcloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and small teams use this skill to inspect and operate cloud servers, install and manage databases, apply schemas, configure monitoring and firewalls, and generate operational health reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use powerful cloud credentials and perform privileged server, database, firewall, backup, restore, and reboot actions.

Mitigation: Use least-privilege temporary credentials, keep secrets out of chat transcripts, repositories, and logs, and require human review of execution plans before privileged actions.

Risk: Security evidence flags unsafe validation and transport safeguards for command and SQL execution paths.

Mitigation: Do not use mutation actions in production until command and SQL parameter validation, local-execution fallback behavior, and transport verification are fixed and reviewed.

Risk: Installer scripts download database and monitoring components from external URLs.

Mitigation: Verify installer sources, signatures, checksums, and package repository trust before running installation workflows on managed servers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/feixuelingcloud/skills/goto-cloudserver-manager)
- [Skill README](artifact/README.md)
- [Node Exporter install guide](artifact/monitoring/node_exporter/install_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with execution plans, shell or PowerShell commands, SQL, YAML configuration, and health reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mutating or privileged actions are intended to require confirmation before execution.]

## Skill Version(s):

1.0.6 (source: server release metadata, SKILL.md frontmatter, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
