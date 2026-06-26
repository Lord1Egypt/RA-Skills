## Description: <br>
Backup Clawdbot workspace and config to GitHub with git-crypt encryption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[louzhixian](https://clawhub.ai/user/louzhixian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure encrypted GitHub backups for Clawdbot workspace and configuration directories, then run manual or scheduled backup and restore workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive workspace or configuration data may be committed or pushed before git-crypt is initialized and verified. <br>
Mitigation: Use private repositories, initialize git-crypt before the first commit, and test encryption from a fresh clone before enabling scheduled backups. <br>
Risk: The backup script stages all changes in the workspace and config repositories. <br>
Mitigation: Review `git status` and staged files before enabling cron or other unattended execution. <br>
Risk: Exported git-crypt keys can unlock encrypted backup contents if exposed. <br>
Mitigation: Store exported git-crypt keys in a secure password manager, keychain, or offline storage location. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/louzhixian/git-crypt-backup) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes git-crypt setup, backup, restore, and scheduled execution guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
