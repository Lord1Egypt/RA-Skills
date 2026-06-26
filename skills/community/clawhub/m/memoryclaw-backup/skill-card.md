## Description: <br>
Helps users install and use MemoryClaw to securely back up and restore their OpenClaw setup across machines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iarayan](https://clawhub.ai/user/iarayan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to choose safe MemoryClaw commands for backing up, checking, restoring, or migrating an OpenClaw setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The separate MemoryClaw plugin needs access to local OpenClaw files and network services to perform backups. <br>
Mitigation: Verify that clawhub:memoryclaw is the intended plugin, review the plugin or source when stronger assurance is needed, and only proceed with installation after accepting that trust boundary. <br>
Risk: Backup passphrases and interactive restore or login steps can expose sensitive information if handled through chat. <br>
Mitigation: Keep passphrases out of chat and run login, restore, and first-time setup commands directly in a local terminal. <br>


## Reference(s): <br>
- [MemoryClaw Backup ClawHub Page](https://clawhub.ai/iarayan/memoryclaw-backup) <br>
- [MemoryClaw Plugin Page](https://clawhub.ai/packages/memoryclaw) <br>
- [MemoryClaw Documentation](https://memoryclaw.ai/docs) <br>
- [MemoryClaw Dashboard](https://memoryclaw.ai/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill provides recommended commands and terminal handoff guidance; it does not execute the MemoryClaw plugin itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
