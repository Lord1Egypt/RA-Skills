## Description:

Generates conventional, descriptive commit messages from staged changes, branch diffs, commit ranges, or user-provided diffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, and teams use this skill to draft, rewrite, summarize, or validate Conventional Commits messages from git diffs and commit ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Git diffs may contain private code, secrets, or other sensitive repository context.

Mitigation: Use the skill only in repositories where the agent may read diffs, and review generated messages before committing or sharing them.

## Reference(s):

- [Commit Message Generator on ClawHub](https://clawhub.ai/ericlooi504/skills/git-commit-gen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with Conventional Commits examples and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a proposed commit message, explanation of reasoning, validation feedback, or suggested git commit command for user review.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
