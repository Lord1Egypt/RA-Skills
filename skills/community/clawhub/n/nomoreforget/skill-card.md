## Description: <br>
Helps OpenClaw users diagnose and reduce memory loss, high token usage, and weak memory retrieval by configuring Memory Flush, memory templates, backups, and maintenance scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steventsang18](https://clawhub.ai/user/steventsang18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to configure persistent memory behavior, check memory health, back up and restore local memory files, and get guidance for reducing token-heavy memory usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer changes persistent OpenClaw memory and compaction settings. <br>
Mitigation: Review scripts/install.sh before running it and keep a current backup of ~/.openclaw so configuration changes can be reversed. <br>
Risk: Memory files, daily logs, and backup folders may preserve session notes or sensitive information. <br>
Mitigation: Avoid storing API keys, passwords, or private data in OpenClaw memory, and periodically review or delete memory backups that are no longer needed. <br>
Risk: The restore script can overwrite current local memory files with backup contents. <br>
Mitigation: Confirm the selected backup before restore and make a fresh backup of the current workspace memory before replacing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steventsang18/nomoreforget) <br>
- [Publisher profile](https://clawhub.ai/user/steventsang18) <br>
- [OpenClaw memory architecture](references/architecture.md) <br>
- [OpenClaw memory plugin comparison](references/plugins.md) <br>
- [OpenClaw memory troubleshooting guide](references/troubleshooting.md) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON configuration examples, local memory templates, and shell scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts operate on the user's local ~/.openclaw configuration, workspace memory files, daily logs, and backup folders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
