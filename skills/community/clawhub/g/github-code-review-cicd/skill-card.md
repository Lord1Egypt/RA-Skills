## Description: <br>
Coordinates GitHub repository and PR data collection, AI code review, and GitHub Actions CI/CD workflow generation for PRs, commits, and new projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review GitHub PRs or commits for code quality and security issues, then generate or recommend CI/CD workflows that fit the repository's language, framework, and review findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use the current GitHub CLI login to read repository data and PR diffs. <br>
Mitigation: Run it only against intended repositories and confirm the active GitHub account and repository before execution. <br>
Risk: The skill may post PR comments or propose workflow files without an explicit approval step. <br>
Mitigation: Require manual confirmation before posting PR comments, applying workflow files, or committing generated CI/CD configuration. <br>
Risk: Generated GitHub Actions workflows may not match the repository's deployment, security, or secret-handling requirements. <br>
Mitigation: Review generated YAML carefully, especially permissions, secret usage, deployment targets, and security scan steps, before enabling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/github-code-review-cicd) <br>
- [GitHub CLI](https://cli.github.com/) <br>
- [quack-code-review](https://clawhub.com/skills/quack-code-review) <br>
- [github-actions-generator](https://clawhub.com/skills/github-actions-generator) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown review reports with inline shell commands and GitHub Actions YAML workflow files or recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PR comments, issue findings, remediation guidance, and generated .github/workflows files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
