## Description: <br>
Git Factory guides agents through provisioning and managing isolated Git worktrees for parallel coding tasks, branch cleanup, and pull request submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spaztazim](https://clawhub.ai/user/spaztazim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to isolate parallel repository changes in separate Git worktrees and branches, then stage, commit, push, and open pull requests from those branches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can use the operator's existing Git permissions to commit, push branches, and create pull requests. <br>
Mitigation: Review the target repository, branch, and remote before running any supplied workflow scripts, and run them only in the intended worktree. <br>
Risk: The referenced PowerShell scripts are not included in the package reviewed here. <br>
Mitigation: Inspect any separately supplied provision, finish, list, or cleanup scripts before running them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with PowerShell and Git command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
