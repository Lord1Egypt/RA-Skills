## Description:

Creates or updates reusable AI skills from personal workflows and examples through guided questions, rule synthesis, and evidence-based validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuetsui](https://clawhub.ai/user/fuetsui)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and developers use this Chinese-language skill to turn recurring tasks, existing materials, and personal practices into reusable agent skills, or revise skills as their requirements change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scripts may overwrite source files when input and output paths collide.

Mitigation: Back up inputs, keep input and output directories separate, check paths for collisions, and test on copies first.

Risk: Generated skills or shared packages may expose private source material or credentials.

Mitigation: Review generated files and remove private raw materials and credentials before sharing.

Risk: A passing checker may not cover every applicable requirement or failure case.

Mitigation: Compare required checks with the actual test evidence, and mark missing coverage as unverified.

Risk: An unpinned installation command may retrieve a different release than intended.

Mitigation: Prefer a version-pinned release archive and verify its checksum before installation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fuetsui/skills/personal-skill-builder)
- [Features](docs/FEATURES.md)
- [Known issues](docs/KNOWN-ISSUES.md)
- [Test results](docs/TEST-RESULTS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown and skill files, with optional templates and scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes documented rules, validation results, and unresolved limitations where applicable.]

## Skill Version(s):

1.0.2 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
