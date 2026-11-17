## Description:

GitHub 智能代码审查与 CI/CD 自动化完整工作流，用于在 PR 或提交场景中收集仓库上下文、生成 AI 代码审查报告，并推荐或生成 GitHub Actions CI/CD 工作流。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to review GitHub pull requests or commits for bugs, security issues, logic problems, and code quality concerns. It can also generate or recommend GitHub Actions workflow files based on the project stack and review results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an authenticated GitHub CLI context to post review output to pull requests.

Mitigation: Require a local preview of the review output and explicit confirmation before any PR comment is posted.

Risk: Generated GitHub Actions workflow files can change CI/CD, security scanning, or deployment behavior.

Mitigation: Review generated .github/workflows files before committing them or enabling them in a repository.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/github-code-review-cicd)
- [Publisher profile](https://clawhub.ai/user/zlszhonglongshen)
- [GitHub CLI documentation](https://cli.github.com/)
- [quack-code-review skill](https://clawhub.com/skills/quack-code-review)
- [github-actions-generator skill](https://clawhub.com/skills/github-actions-generator)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown reports with inline shell commands and generated GitHub Actions YAML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May post review output as a pull request comment and may produce .github/workflows files for CI, security scanning, or deployment.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
