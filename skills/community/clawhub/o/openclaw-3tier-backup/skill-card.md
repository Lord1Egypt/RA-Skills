## Description: <br>
Automated backup in 3 layers: daily timestamped snapshots, secondary drive mirror, and emergency conversation export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users managing local AI workspaces use this skill to set up daily snapshots, optional drive mirroring, and an emergency local chat file for recovery scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Destructive restore commands can overwrite or delete files when paths are wrong, especially when using mirror-style restore commands. <br>
Mitigation: Verify source and destination paths before restore, and avoid robocopy /MIR until the user understands that it may delete destination files. <br>
Risk: A scheduled backup script can copy sensitive workspace data into backup locations. <br>
Mitigation: Treat backup folders, mirrors, removable drives, and exported recovery files as sensitive copies of the workspace. <br>
Risk: User-created automation may behave differently from the guide if the PowerShell script is changed before scheduling. <br>
Mitigation: Review any daily-backup.ps1 created from the guide before registering it as a scheduled task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/openclaw-3tier-backup) <br>
- [Publisher profile](https://clawhub.ai/user/TheShadowRose) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with PowerShell command snippets and a standalone HTML emergency chat file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Backup and restore paths must be customized by the user before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
