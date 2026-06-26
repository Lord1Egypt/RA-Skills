## Description: <br>
Provides local Git workflow guidance for branching, syncing, committing, pushing, and preparing pull or merge requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhulaoqi](https://clawhub.ai/user/zhulaoqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project maintainers use this skill to plan and execute routine local Git workflows, including creating issue branches, reviewing status and diffs, committing changes, syncing from main, and preparing pull or merge requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose branch, commit, pull, rebase, branch-switch, or push operations that change the local repository or remote history. <br>
Mitigation: Check the current branch, remote, and diff first, and require explicit confirmation before running repository-changing Git commands. <br>
Risk: Git workflow advice can be incorrect for a repository's branch policy or merge process. <br>
Mitigation: Review proposed commands against the project's contribution rules before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhulaoqi/git-hub-issus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose repository-changing Git commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
