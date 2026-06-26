## Description: <br>
Verifies workspace state and staged changes as a read-only preflight before commits or PRs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill before commit, pull request, or release-note workflows to inspect repository status, staged changes, diff statistics, and detailed diffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is described as read-only but includes workflow steps that can format files or change staged state. <br>
Mitigation: Treat mutating actions as proposed commands and require explicit confirmation before formatting, staging, unstaging, or aborting merges. <br>
Risk: A review can be misleading if status or diffs are collected from the wrong repository, branch, or staging state. <br>
Mitigation: Confirm the working directory, branch, upstream, and staged versus unstaged changes before relying on the review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-sanctum-git-workspace-review) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/athola) <br>
- [Project homepage from ClawHub metadata](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and review checkpoints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can lead an agent to run formatters and adjust staged files; require approval before mutating commands.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
