## Description: <br>
Git Tool provides useful Git commands for repository management, including branch, history, stash, diff, and commit workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run common Git repository-management workflows through an agent, including checking status, viewing logs and diffs, creating commits, managing branches, and stashing changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: State-changing Git actions can modify repository contents or history, including add, commit, stash-pop, push, and pull. <br>
Mitigation: Review or explicitly approve state-changing commands before execution, especially in repositories with configured remotes or saved credentials. <br>
Risk: Remote Git operations can interact with configured remotes using existing local credentials. <br>
Mitigation: Confirm the target remote and branch before running push or pull commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/git-tool) <br>
- [Publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Git command output from the active workspace when the helper script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
