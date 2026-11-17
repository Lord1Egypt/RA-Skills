## Description:

将本地创建或修改的 Claude Code 技能自动同步到 GitHub 仓库。支持增量同步、单技能同步、自动生成 README.md。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuiilabs](https://clawhub.ai/user/kuiilabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to synchronize locally created or modified Claude Code skills to a GitHub repository, either incrementally or one skill at a time. It also helps generate repository README content and troubleshoot GitHub token permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local skill files can be uploaded to GitHub, including files the user did not intend to publish.

Mitigation: Review the selected skill directory and destination repository before syncing, and use a token limited to the intended private repository when possible.

Risk: GitHub tokens may be exposed when passed on the command line or granted broad repository permissions.

Mitigation: Prefer environment variables or a secrets manager, use a fine-grained token scoped to one repository, and rotate tokens regularly.

Risk: The cleanup script can delete remote repository content after building a deletion list.

Mitigation: Run cleanup only after reviewing the deletion list, use dry-run mode first, and keep a backup or recovery plan for the repository.

Risk: Supplying an unverified skill name can cause the sync workflow to target an unintended local directory.

Mitigation: Use --skill only with a simple, verified skill directory name from the local skills folder.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kuiilabs/skills/github-sync-skill)
- [GitHub Token Troubleshooting](references/token-troubleshooting.md)
- [GitHub Personal Access Tokens documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [GitHub REST API rate limiting documentation](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run GitHub API shell workflows that read local skill files, upload repository contents, update README.md, and print sync or token-validation reports.]

## Skill Version(s):

2.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
