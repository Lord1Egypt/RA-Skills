## Description:

Standardized Git commit message templates using changelog-style categories for creating commits, standardizing commit history, and choosing Added, Changed, Deprecated, Removed, or Fixed categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ihomway](https://clawhub.ai/user/ihomway)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create consistent Git commit messages, either by following the documented template manually or by using the bundled Python helper to preview and create structured commits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can create local Git commits from staged repository changes.

Mitigation: Review staged files and the generated commit preview before confirming commit creation.

Risk: Hook-skipping guidance can bypass normal repository checks when used carelessly.

Mitigation: Keep standard Git hooks enabled by default and use hook skipping only when repository policy allows it.

## Reference(s):

- [Commit Message Examples and Guidelines](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with Git command examples and optional Python helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper can create local Git commits from staged changes after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
