## Description: <br>
Verifies workspace state and staged changes as a read-only preflight for commits, pull requests, and release preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill before commits, pull requests, or release notes to inspect repository state, staged changes, and relevant diffs. It helps confirm that the intended work is staged and that code quality checks have been considered. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is described as read-only but can lead an agent to stage or unstage files and run formatting fixes. <br>
Mitigation: Require explicit confirmation before staging, unstaging, formatting, or applying fixes, and review git status and diffs before continuing. <br>
Risk: Project-defined formatting and lint commands may modify files or execute repository-specific tooling. <br>
Mitigation: Run the skill only in trusted repositories or an isolated workspace, and inspect the relevant build scripts before allowing automated commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-sanctum-git-workspace-review) <br>
- [ClawHub metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>
- [Git commands reference](modules/git-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and a progress checklist] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve git status, diff, staging, formatting, and lint commands depending on agent execution policy.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
