## Description:

Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollis9087](https://clawhub.ai/user/hollis9087)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and other external users use this skill to install and run the blogwatcher CLI for tracking RSS/Atom feeds, scanning for new articles, and managing read status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and uses a third-party blogwatcher CLI from a mutable Go @latest target.

Mitigation: Prefer a pinned release or commit when possible, and run the CLI with normal user privileges.

Risk: The skill guides agents to track and scan user-provided blog or RSS/Atom feed URLs through the external CLI.

Mitigation: Review feed URLs before use and avoid running the CLI with elevated access or from sensitive working directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hollis9087/skills/holli-blogwatcher)
- [blogwatcher homepage](https://github.com/Hyaxia/blogwatcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include install and usage commands for the blogwatcher CLI.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
