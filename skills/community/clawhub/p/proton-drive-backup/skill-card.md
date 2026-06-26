## Description: <br>
Automates backups to a local Proton Drive sync folder with retention rules for OpenClaw configs, memory files, content drafts, media, and optional Docker volume backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to generate or run a backup workflow that copies local workspace state into Proton Drive's desktop sync folder while pruning older backup copies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The backup workflow can copy sensitive OpenClaw configuration, memory, agent, draft, media, and Docker volume data into cloud-synced storage. <br>
Mitigation: Review the configured source paths and file categories before running the skill, and run it only when those files are intended to be backed up through Proton Drive. <br>
Risk: Retention cleanup automatically deletes older backup copies for daily memory, media, and Docker volume backups. <br>
Mitigation: Confirm the retention windows match recovery needs before scheduling recurring runs or using the optional Docker backup mode. <br>
Risk: The script assumes a hardcoded Proton Drive local sync folder and OpenClaw workspace layout. <br>
Mitigation: Verify the local Proton Drive and OpenClaw paths before execution, especially on systems with different account names or folder locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/proton-drive-backup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, rsync, docker for optional volume backups, and the Proton Drive desktop app with the expected local sync folder.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
