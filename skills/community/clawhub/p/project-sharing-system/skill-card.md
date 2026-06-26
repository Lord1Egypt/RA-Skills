## Description: <br>
Project Sharing System helps agents share project status, discover active work, sync updates, and keep project history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clementgu](https://clawhub.ai/user/clementgu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain a shared project-status workspace for multiple agents, including project listing, updates, summaries, snapshots, and automatic backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent project files and backups may retain local project state, history, and operational notes. <br>
Mitigation: Install only where that data is acceptable to persist, and review or reset the bundled projects_status.json before relying on it. <br>
Risk: Local helper scripts write project data, regenerate Markdown views, and run backup commands in the configured workspace. <br>
Mitigation: Use the skill in a trusted workspace and prevent untrusted users from modifying the installed scripts or project data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/clementgu/project-sharing-system) <br>
- [Publisher profile](https://clawhub.ai/user/clementgu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, Markdown status snapshots, JSON project data, shell command examples, and an HTML dashboard] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates persistent local project-state files and backup snapshots.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
