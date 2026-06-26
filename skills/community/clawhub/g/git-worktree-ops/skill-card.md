## Description: <br>
Helps agents manage parallel development workspaces with Git worktree commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soponcd](https://clawhub.ai/user/soponcd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create, list, and remove isolated Git worktree workspaces for parallel development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced tools/git_worktree_manager.sh helper script was not included in the reviewed package. <br>
Mitigation: Inspect and verify the local helper script before using this skill's commands. <br>
Risk: Remove operations can delete local worktrees and may discard needed files if the wrong target is selected. <br>
Mitigation: Confirm the target worktree and check for uncommitted or needed files before running remove commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/soponcd/git-worktree-ops) <br>
- [Declared Homepage](https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/git-worktree-ops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is centered on local Git worktree operations and the referenced helper script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
