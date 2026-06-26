## Description: <br>
Git Helper guides agents through status checks, staging, commits, pushes, pulls, rebases, diffs, logs, and branch operations using safe Git workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dougchambes](https://clawhub.ai/user/dougchambes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to help agents operate Git repositories consistently, including checking status, staging changes, composing conventional commits, synchronizing branches, and handling rebases or merges with explicit safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Git commands can change repository state, branch history, or remotes if followed without review. <br>
Mitigation: Review git status, diffs, staged files, target branch, and remote before allowing commits, pushes, rebases, hard resets, or force pushes. <br>
Risk: History-rewriting or destructive operations can disrupt shared work. <br>
Mitigation: Require explicit user approval for destructive or history-rewriting actions and avoid force pushes unless the user authorizes them. <br>


## Reference(s): <br>
- [Git Workflows Reference](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown with inline Git shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No generated files are required; destructive or history-rewriting Git operations require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
