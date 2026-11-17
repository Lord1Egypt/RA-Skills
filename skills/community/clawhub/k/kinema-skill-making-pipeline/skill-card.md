## Description:

Kinema's Skill Making Pipeline defines a cross-platform skill development and publishing workflow for Codex, Claude Code, GitHub Release, and ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeshunee](https://clawhub.ai/user/leeshunee)

### License/Terms of Use:

GNU General Public License v3.0

## Use Case:

Developers and maintainers use this skill to create, version, validate, publish, and synchronize cross-platform skills across Codex, Claude Code, GitHub Release, and ClawHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ClawHub API fallback can upload sensitive local files if the package contents are not reviewed first.

Mitigation: Review the exact files to be uploaded and exclude .env files, credentials, tokens, local configuration, and private datasets before using the fallback.

Risk: Fallback and troubleshooting examples include cache cleanup or sudo/global install commands that can affect local agent environments.

Mitigation: Confirm resolved paths and obtain explicit approval before running cache cleanup, sudo, or global install commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leeshunee/skills/kinema-skill-making-pipeline)
- [Onboarding Guide](references/ONBOARDING.md)
- [Release Process](references/release-process.md)
- [Marketplace Publishing](references/marketplace-publishing.md)
- [ClawHub API Fallback](references/clawhub-api-fallback.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes release checklists, platform-specific installation commands, and version validation guidance.]

## Skill Version(s):

1.11.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
