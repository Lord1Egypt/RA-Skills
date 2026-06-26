## Description: <br>
在 Obsidian 库（Markdown + Git）内检索笔记、创建与管理 .md；用 Git 查看历史与提交变更，并管理远程与同步（fetch/pull/push）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cfddd](https://clawhub.ai/user/cfddd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and agent operators use this skill to manage an Obsidian Markdown vault through safe file operations and Git-based history, remote setup, and synchronization workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may edit or synchronize the wrong vault if the resolved path is not checked. <br>
Mitigation: Verify the resolved vault path before file edits, Git initialization, commits, pulls, pushes, or scheduled sync setup. <br>
Risk: Git commits or pushes may publish unintended notes or local changes. <br>
Mitigation: Review Git status and diffs before staging, committing, or pushing, and confirm the intended file scope. <br>
Risk: Remote authentication can expose excessive repository or account permissions. <br>
Mitigation: Use narrow SSH deploy keys or minimal PAT scopes, and do not store tokens or private keys inside the vault. <br>
Risk: Recurring cron sync can continue making networked Git operations after setup. <br>
Mitigation: Enable cron only after explicit consent and only when the user understands how to inspect, pause, or disable the job. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cfddd/obsidian-git-vault) <br>
- [Git remote wizard](git-remote-wizard.md) <br>
- [Vault sync SOP](vault-sync-sop.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file path references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify Markdown notes and propose Git commands for status, commits, pulls, pushes, remote setup, conflict handling, and scheduled sync setup.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
