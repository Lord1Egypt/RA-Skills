## Description: <br>
Automates GitHub contribution workflows, including issue discovery, fork synchronization, branch setup, and pull request preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linux2010](https://clawhub.ai/user/linux2010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external contributors use this skill to find maintainer-approved issues, prepare clean fork branches, and create pull requests for open source repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Destructive Git cleanup and reset steps can discard local commits or untracked work. <br>
Mitigation: Run the workflow only in a clean, backed-up worktree or disposable clone; review commands first and prefer dry-run cleanup checks. <br>
Risk: Push and history-rewrite steps can affect the wrong branch or overwrite pull request history. <br>
Mitigation: Confirm remotes, branch names, and ownership before pushing; use force-with-lease instead of force pushes when history rewriting is required. <br>


## Reference(s): <br>
- [ClawHub GitHub Contribution release](https://clawhub.ai/linux2010/github-contribution) <br>
- [GitHub contribution workflow artifact](artifact/github-contribution-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and Bash workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should be reviewed before use, especially cleanup, reset, and push operations.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
