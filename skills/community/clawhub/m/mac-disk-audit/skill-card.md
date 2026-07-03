## Description: <br>
Mac Disk Audit helps agents scan Mac disk usage, identify large files and common high-usage areas, and produce tiered cleanup recommendations with commands for the user to review before running. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guipi888](https://clawhub.ai/user/guipi888) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Mac users and developers use this skill to audit local disk usage, find large files, caches, backups, and development artifacts, and receive a structured cleanup plan. It is intended to provide analysis and user-reviewed commands rather than perform automatic deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Permanent-delete commands such as rm -rf or sudo rm -rf can remove files irreversibly if copied without careful review. <br>
Mitigation: Review each command and path manually, prefer Finder or Trash-based cleanup, and keep backups before deleting data. <br>
Risk: Cleanup recommendations may conflict with the skill's safety posture if commands are treated as automatic instructions rather than proposals. <br>
Mitigation: Require explicit user confirmation before running any cleanup command and list the affected paths, sizes, and recovery options. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guipi888/mac-disk-audit) <br>
- [Publisher profile](https://clawhub.ai/user/guipi888) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are presented for user review and confirmation; the skill is not intended to delete files automatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
