## Description: <br>
Advanced Git operations as tools: interactive rebase with autosquash, worktree management, reflog recovery, subtree and submodule handling, cherry-pick across forks, PR automation with human-written intent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neroagent](https://clawhub.ai/user/neroagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to run advanced Git workflows, including rebase planning, worktree setup, reflog recovery, subtree imports, pull request creation, and changelog generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad repository and GitHub authority through unsafe shell command construction and weak safeguards. <br>
Mitigation: Use only in repositories where branch rewrites, worktree creation, subtree imports, and GitHub PR creation are acceptable; avoid untrusted branch names, paths, URLs, tags, titles, and PR bodies until shell command handling is fixed. <br>
Risk: Some workflows can rewrite branches or alter repository structure. <br>
Mitigation: Review the target repository state and command intent before execution, and keep recoverable backups or remote refs for important work. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/neroagent/git-workflows-advanced) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON tool responses with commit lists, command guidance, pull request URLs, or markdown changelog content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some operations require Git, and pull request creation requires an authenticated GitHub CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
