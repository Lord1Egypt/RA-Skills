## Description: <br>
Backup and restore all agent files and configurations to fully migrate an OpenClaw agent with local packaging, path mapping, and integrity verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junmopho](https://clawhub.ai/user/junmopho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create local backups of agent state, workspace files, credentials, sessions, memory, and configuration, then restore that agent state in another environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may contain live API keys, login sessions, personal memory, and workspace files. <br>
Mitigation: Store backup archives encrypted, do not share them, and inspect archive contents before restore. <br>
Risk: Restore operations can replace current configuration and workspace state while documented safeguards may be incomplete. <br>
Mitigation: Keep an independent backup, verify archive integrity before restore, and confirm the target environment before overwriting files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/junmopho/junmopho-soul-transfer) <br>
- [Restore Reference](references/restore.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and backup or restore paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe archive contents, integrity checks, safety backups, path mapping, and post-restore verification steps.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
