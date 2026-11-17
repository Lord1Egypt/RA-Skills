## Description:

Helps agents split staged Git changes into focused commits, generate conventional commit messages, and optionally prompt for explicitly confirmed post-commit sync or subtree-push workflows when the repository is configured for them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to organize staged repository changes into multiple logical commits with standardized commit messages. It is intended for commit preparation and local Git history hygiene, not for branch, PR, merge, push, or issue-closing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Git path handling can mis-handle specially named repository files and mutate the repository in unintended ways.

Mitigation: Use the skill only in trusted repositories, review proposed groups before committing, prefer dry-run or interactive review, and avoid --yes until Git path handling uses -- separators and NUL-delimited filename parsing.

Risk: Optional sync or subtree workflows can upload skill contents or push to remotes after commits when repository configuration enables those paths.

Mitigation: Proceed with sync, publish, or subtree push prompts only after explicit confirmation, and review the affected files and destination before confirming.

## Reference(s):

- [Skill homepage](https://github.com/cat-xierluo/legal-skills)
- [Commit Types Reference](references/commit-types.md)
- [Conventional Commits Reference](references/conventional-commits.md)
- [ClawHub Sync Check](references/clawhub-sync-check.md)
- [Subtree Push Check](references/subtree-push-check.md)
- [Message Data](references/message-data.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown and terminal text with conventional commit messages, grouped file summaries, and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Git commits and, only after explicit user confirmation and matching repository configuration, may prompt for publishing or subtree push follow-up actions.]

## Skill Version(s):

1.4.2 (source: server release evidence, SKILL.md frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
