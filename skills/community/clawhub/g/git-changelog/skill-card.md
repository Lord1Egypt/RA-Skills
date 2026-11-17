## Description:

Auto-generate beautiful changelogs from git history, grouped by conventional commit types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fratua](https://clawhub.ai/user/fratua)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to generate categorized Markdown changelogs or release notes from git commit history, including conventional commit groupings and breaking-change callouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads git history, including commit messages, author names, dates, and hashes from the current repository.

Mitigation: Run it only in repositories where that git metadata is appropriate to inspect or summarize.

Risk: The skill may modify CHANGELOG.md when file output is requested.

Mitigation: Review generated changelog content before committing changes, and request chat-only output when file modification is not desired.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print changelog content to chat or write/prepend CHANGELOG.md when requested.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
