## Description: <br>
Git Log Tracker records Git commit metadata into a local SQLite index through a post-commit hook and provides CLI commands to query, list, summarize, update, and delete records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeshunee](https://clawhub.ai/user/leeshunee) <br>

### License/Terms of Use: <br>
GNU General Public License v3.0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and manage Git post-commit hooks, maintain a local commit-history index across repositories, and query commit records by hash, repository, author, date, branch, or label. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent Git hook and global Git configuration changes. <br>
Mitigation: Confirm the exact repositories before using scan, batch install, or global mode, and review hook status after installation. <br>
Risk: The local SQLite index can contain sensitive repository paths, author emails, commit subjects, and commit bodies. <br>
Mitigation: Avoid indexing sensitive repositories and use exclude rules before enabling hooks broadly. <br>
Risk: Reset and delete operations can remove local commit-index data. <br>
Mitigation: Back up ~/.commit-logs before using reinstall or destructive record-management commands. <br>


## Reference(s): <br>
- [Git Log Tracker Onboarding](references/ONBOARDING.md) <br>
- [ClawHub skill page](https://clawhub.ai/leeshunee/git-log-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local Git hooks, Git global template settings, and files under ~/.commit-logs.] <br>

## Skill Version(s): <br>
0.6.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
