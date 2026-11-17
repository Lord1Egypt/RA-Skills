## Description:

Git Commit Helper Pro helps agents generate Conventional Commits messages, inspect repository status and diffs, list branches, view recent history, and create commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software engineering agents use this skill to summarize Git changes, generate conventional commit messages, inspect branches and history, and automate simple commit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The commit helper can stage every changed, deleted, and untracked file before committing, which may include secrets or unrelated work.

Mitigation: Review git status, git diff, and the staged file list before using commit automation; avoid running it in repositories with sensitive or unrelated changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-git-commit-helper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional Python code examples and Git command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute Git commit workflows depending on the hosting agent's tool permissions.]

## Skill Version(s):

2.0.0 (source: release evidence, SKILL.md frontmatter, hub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
