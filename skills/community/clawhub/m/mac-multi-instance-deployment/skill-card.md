## Description:

Public-safe Mac multi-instance deployment skill for generic OpenClaw-style workspace layout, boundary notes, sample config, and pack validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoma970](https://clawhub.ai/user/guoma970)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan generic Mac multi-instance OpenClaw-style workspace layouts, keep public and private boundaries clear, and validate release packs before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested shell commands could affect a user's local repository or generated release pack.

Mitigation: Review commands before running them and use the documented dry-run and list checks before publishing.

Risk: Private paths, secrets, account data, or runtime state could be accidentally included in public materials.

Mitigation: Use placeholder paths, keep private files out of public packs, and run validation before release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guoma970/skills/mac-multi-instance-deployment)
- [Publisher Profile](https://clawhub.ai/user/guoma970)
- [README](artifact/README.md)
- [Publishing Summary](artifact/PUBLISHING.md)
- [Release 1.0.4](artifact/releases/1.0.4.md)
- [Customization Guide](artifact/CUSTOMIZATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public-safe guidance emphasizes placeholder paths, generic instance labels, and local handling of private runtime state.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release metadata, README, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
