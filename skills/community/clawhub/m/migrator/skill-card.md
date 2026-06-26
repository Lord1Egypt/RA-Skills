## Description: <br>
Securely migrate OpenClaw Agent config, memory, and skills to a new machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenjie2024](https://clawhub.ai/user/wenjie2024) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to export encrypted OpenClaw agent state from one machine and restore it on another while preserving configuration, memory, skills, and path metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Migration archives can contain sensitive OpenClaw state such as configuration, memory, skills, and authentication material. <br>
Mitigation: Use strong unique passwords, keep .oca archives private, and avoid exposing passwords through shell history where possible. <br>
Risk: Importing an archive can overwrite files under the selected destination, including a user's home directory. <br>
Mitigation: Back up existing OpenClaw files and restore first to a temporary destination before importing into the home directory. <br>
Risk: Archives from untrusted sources may restore unwanted or unsafe agent state. <br>
Mitigation: Import only archives the user created or fully trusts, and review restored content before relying on it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wenjie2024/migrator) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference encrypted .oca archives, destination paths, source directories, and password handling practices.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, package.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
