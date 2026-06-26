## Description: <br>
Helps agents handle Git worktree development tasks by identifying the current repository and request, checking worktree status, making scoped code changes, and summarizing results without crossing worktree boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidongkl](https://clawhub.ai/user/weidongkl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to manage parallel Git worktree development tasks, inspect the active worktree, make minimal scoped changes, and prepare implementation summaries or commit suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may propose or make code changes in the current Git worktree that are incorrect or broader than intended. <br>
Mitigation: Review proposed file changes, diffs, and summaries before committing or relying on the result. <br>
Risk: Git commands can affect local worktree state, especially destructive operations such as hard resets or cleans. <br>
Mitigation: Only approve destructive Git commands when explicitly intended, and verify the branch and worktree status first. <br>
Risk: Parallel worktree workflows can accidentally touch the wrong repository, branch, or request scope. <br>
Mitigation: Confirm the current directory, branch, and parsed worktree purpose before allowing edits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weidongkl/git-worktree) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands, file summaries, risk notes, and commit message suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should stay scoped to the current worktree and avoid unrelated repository or branch changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
