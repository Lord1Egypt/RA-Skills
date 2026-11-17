## Description:

Learning Evolution creates evidence-based learning reviews for skills by analyzing usage patterns, tracking effectiveness, and planning evolutions with local Markdown templates and data integrity guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to create verified-data templates for reviewing skill usage, measuring effectiveness, and planning evidence-backed skill improvements before publishing changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Predictable local Markdown report paths can overwrite existing files in shared or untrusted directories.

Mitigation: Run the generators only in a private, trusted directory and set LEARNING_DATA_DIR deliberately when a specific report location is needed.

Risk: Blank template fields can be mistaken for measured usage, effectiveness, or feedback data.

Mitigation: Fill metrics only from verified logs, direct feedback, or observed outcomes before using the reports to change a published skill.

## Reference(s):

- [Skill documentation](artifact/SKILL.md)
- [README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/learning-evolution)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown templates created as local files, with shell commands and concise review guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated templates leave analytics and recommendations blank until users fill them from verified logs, direct feedback, or observed outcomes.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
