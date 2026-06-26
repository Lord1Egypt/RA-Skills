## Description: <br>
Automates OpenClaw workspace backups with SQLite database export, optional NAS transfer, and Git commit/push guidance for versioned recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lancelot3777-svg](https://clawhub.ai/user/lancelot3777-svg) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to configure manual or scheduled backups for an OpenClaw workspace, including database copies, optional NAS storage, and GitHub-based version control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The backup scripts can copy workspace and database data to an author-specific NAS path if run unchanged. <br>
Mitigation: Review and edit all paths and destinations before installing or running; narrow the backup scope and remove author-specific NAS settings. <br>
Risk: Backups may include secrets, private databases, or sensitive workspace files. <br>
Mitigation: Exclude secrets and private databases unless intentionally included, and use only private GitHub or NAS destinations you control. <br>
Risk: The suggested cron setup can repeatedly run backup, commit, push, and transfer commands automatically. <br>
Mitigation: Do not enable cron until the command chain is reviewed, tested manually, and limited to approved backup targets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lancelot3777-svg/openclaw-backup-guide) <br>
- [Release changelog](https://github.com/lancelot3777-svg/openclaw-backup-guide) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and backup scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Node.js and shell script files that require local path and destination review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
