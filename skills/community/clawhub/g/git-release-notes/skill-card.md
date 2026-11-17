## Description:

Generate polished release notes and changelogs from git history by analyzing commits between tags or refs, categorizing changes, and producing formatted release notes in multiple styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release managers use this skill to turn git commit history between refs into release notes, changelog entries, GitHub release text, or team announcements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can execute local commands if given a maliciously crafted git reference.

Mitigation: Use only trusted repositories and trusted refs unless the helper is patched to pass refs to Python as data through argv or environment variables.

Risk: Generated release notes may misclassify commits or overstate changes when commit messages are ambiguous.

Mitigation: Review the generated notes against the commit list before publishing release documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/git-release-notes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown release notes, compact summaries, changelog entries, or announcement text with optional shell commands for gathering commit data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can organize output by category, author, scope, selected format, included categories, contributors, and pull request links.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
