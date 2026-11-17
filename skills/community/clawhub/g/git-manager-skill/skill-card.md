## Description:

Git Manager helps agents perform Git repository operations including clone, pull, merge, rebase, commit, staging, Git LFS management, reflog recovery, worktree management, grep search, cherry-pick, revert, bisect, and batch operations across GitHub, GitLab, Gitea, Bitbucket, and Azure DevOps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyjnicemoe](https://clawhub.ai/user/zyjnicemoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to let an agent manage single-repository and multi-repository Git workflows, including synchronization, branching, history inspection, LFS setup, and batch clone or pull operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository access tokens may be exposed through shell history, process listings, or persistent credential storage.

Mitigation: Use narrowly scoped, read-only, revocable tokens from environment variables or a secure credential manager, and avoid passing tokens directly on the command line.

Risk: Plaintext HTTP or untrusted custom GitLab and Gitea hosts can expose repository credentials or clone traffic.

Mitigation: Use trusted HTTPS or SSH endpoints and verify custom host ownership before providing credentials.

Risk: Git operations such as rebase, reset, clean, revert, cherry-pick, and batch pull can change repository history or working trees.

Mitigation: Review generated commands before execution, prefer dry-run or status checks where available, and keep backups or remote refs for important branches.

## Reference(s):

- [Git Manager API Reference](references/api_reference.md)
- [Git Manager Usage Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/zyjnicemoe/skills/git-manager-skill)
- [Publisher Profile](https://clawhub.ai/user/zyjnicemoe)
- [Author Homepage](https://zyjblogs.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Python CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON output instructions when using supported script options.]

## Skill Version(s):

2.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
