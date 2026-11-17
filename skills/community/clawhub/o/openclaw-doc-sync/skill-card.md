## Description:

Post-release documentation sync skill that aligns README, ARCHITECTURE, CONTRIBUTING, CLAUDE.md, TODOs, changelog wording, and optional version updates with actual project changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill after code changes and before pull request merge to keep project documentation, changelogs, TODOs, and version notes aligned with the actual diff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make documentation changes and create a documentation commit.

Mitigation: Review the final summary and git diff before pushing, especially when changelog, TODO, or version files are touched.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and direct file-edit guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May edit documentation files and create a scoped documentation commit when run in a repository.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
