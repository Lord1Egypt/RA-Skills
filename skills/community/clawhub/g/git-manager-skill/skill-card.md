## Description: <br>
Git Manager helps agents perform Git repository operations including cloning, pulling, merging, rebasing, committing, staging, Git LFS management, reflog recovery, worktree management, grep search, cherry-pick, revert, bisect, and batch operations across GitHub, GitLab, Gitea, Bitbucket, and Azure DevOps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zyjnicemoe](https://clawhub.ai/user/zyjnicemoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to automate single-repository and multi-repository Git workflows, including batch clone and pull, branch and history operations, Git LFS setup, and recovery-oriented commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run Git commands that make lasting repository changes, including reset, clean, rebase, push, remote changes, and batch updates. <br>
Mitigation: Require explicit review before executing destructive or broad-scope operations, and use dry-run modes, limits, filters, backups, or temporary branches before bulk changes. <br>
Risk: Repository platform access may require sensitive tokens or credentials. <br>
Mitigation: Use least-privilege tokens through a credential helper or protected environment variable, and avoid placing tokens in command lines or clone URLs. <br>
Risk: LFS migration workflows may alter repository history or content storage in ways that are difficult to undo. <br>
Mitigation: Review LFS migration commands before execution and avoid the LFS migrate --to git path until the flagged behavior is fixed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zyjnicemoe/git-manager-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/zyjnicemoe) <br>
- [API Reference](references/api_reference.md) <br>
- [Usage Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and command-line arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON output instructions for supported batch clone workflows.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
