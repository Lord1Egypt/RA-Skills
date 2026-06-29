## Description: <br>
A multi-cloud server operations skill for Alibaba Cloud, Tencent Cloud, and Huawei Cloud servers that supports database installation, schema creation, monitoring checks, and health reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feixuelingcloud](https://clawhub.ai/user/feixuelingcloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to manage cloud servers through OpenClaw conversations, including status checks, database setup, schema deployment, monitoring setup, backups, restores, and health reports. It is intended for environments where operators can review and confirm infrastructure-changing actions before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use powerful cloud and server credentials to perform infrastructure-changing actions. <br>
Mitigation: Use short-lived, least-privilege credentials and avoid sharing production root or administrator secrets in chat. <br>
Risk: Firewall, security-group, backup, restore, reboot, and database changes can affect production availability or exposure. <br>
Mitigation: Review the skill policies, set production servers to a strict environment, and manually inspect each change plan before confirming execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/feixuelingcloud/skills/goto-cloudserver-manager) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Node Exporter install guide](monitoring/node_exporter/install_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, operational plans, shell commands, SQL, and YAML configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations require confirmation, and destructive actions are blocked by policy.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence, frontmatter, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
