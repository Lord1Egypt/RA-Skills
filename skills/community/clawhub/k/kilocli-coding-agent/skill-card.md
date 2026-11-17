## Description:

Run Kilo CLI via background process for programmatic control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nathansebhastian](https://clawhub.ai/user/nathansebhastian)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to launch and monitor Kilo CLI coding tasks, PR reviews, issue fixes, and GitHub workflow work from an OpenClaw environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous Kilo CLI subprocesses may make repository changes or create GitHub output that the user did not fully inspect.

Mitigation: Review all diffs, generated files, PRs, and comments before pushing or publishing changes.

Risk: A broad GitHub token can grant more repository or workflow access than a task needs.

Mitigation: Use a fine-grained, repository-scoped GitHub token and avoid actions:write unless the current task requires it.

Risk: PR bodies, comments, prompts, logs, private paths, or internal context may expose sensitive information.

Mitigation: Sanitize generated GitHub content and session logs before posting or sharing them.

## Reference(s):

- [Kilo CLI Coding Agent on ClawHub](https://clawhub.ai/nathansebhastian/skills/kilocli-coding-agent)
- [GitHub CLI installation](https://github.com/cli/cli#installation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Kilo CLI, git, GitHub CLI, tmux, and a repository-scoped GITHUB_TOKEN.]

## Skill Version(s):

0.0.9 (source: release metadata, SKILL.md frontmatter, claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
