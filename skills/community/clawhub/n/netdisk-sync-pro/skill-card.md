## Description: <br>
网盘同步专家 helps agents manage Baidu Netdisk files under /apps/bdpan/ using bdpan CLI workflows for upload, download, transfer, sharing, search, batch handling, incremental sync, integrity checks, and agent memory backup or restore. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to operate Baidu Netdisk through natural language while the agent prepares or runs bdpan shell commands. It is suited for file upload and download management, large-file downloads, share transfer, batch file operations, incremental sync, and agent memory backup or restore. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan says the skill needs review because high-impact actions are under-scoped or inconsistently confirmed. <br>
Mitigation: Review the skill before installation and require explicit confirmation for writes, deletion, overwrite downloads, public sharing, installation, update, and memory restore operations. <br>
Risk: The skill can mutate remote Baidu Netdisk files, create public share links, and overwrite local agent-memory files. <br>
Mitigation: Run it only where command execution and remote file mutation are acceptable; keep operations constrained to /apps/bdpan/, preview restore impacts, and rely on the documented safety-net backup before memory restore. <br>
Risk: Install and update scripts download or change local tooling used by the agent. <br>
Mitigation: Use install or update flows only after user direction, avoid silent updates, and review installer behavior in sensitive environments. <br>
Risk: Authentication material for bdpan may be sensitive. <br>
Mitigation: Do not read or expose ~/.config/bdpan/config.json or token values; use the documented login script flow instead. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/thcjp/skills/netdisk-sync-pro) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger command execution through bdpan CLI and bash scripts when the hosting agent has execution permission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
