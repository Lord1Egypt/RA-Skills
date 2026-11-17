## Description:

Generates README.md and CHANGELOG.md drafts for software projects from project details, feature lists, and commit-style update text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moodsir](https://clawhub.ai/user/moodsir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create standard project README and changelog drafts, classify commit-style updates, and calculate semantic version bumps for release documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may misunderstand setup or behavior if they cannot review the Chinese-language documentation.

Mitigation: Review the artifact README, SKILL, and platform documentation before installing or invoking the skill.

Risk: A mutable npx installer command may install an unexpected release.

Mitigation: Use a pinned or otherwise verified ClawHub installer where possible.

Risk: Broad trigger phrases for documentation generation may invoke the skill accidentally.

Mitigation: Configure platform trigger phrases specifically when accidental invocation would be disruptive.

Risk: Generated README and changelog drafts can be incomplete or inaccurate when project metadata or commit text is incomplete.

Mitigation: Review generated Markdown before publishing it in a repository or release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/moodsir/skills/moodsir-auto-readme-changelog)
- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Guidance]

**Output Format:** [Markdown and plain text, with CLI examples and Python function outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces README and changelog drafts that should be reviewed before publication.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
