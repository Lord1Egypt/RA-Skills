## Description:

Ghost CMS helps agents provide guidance for Ghost installation, theme development, CLI usage, Content and Admin API integration, GScan validation, dynamic routing, publishing, deployment, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[themeix](https://clawhub.ai/user/themeix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and content engineering teams use this skill to build and maintain Ghost CMS sites, themes, integrations, and deployment workflows. It is also useful when an agent needs to explain or draft Ghost CLI commands, Handlebars templates, API examples, theme configuration, or validation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some examples install npm tools globally or request the latest package versions, which can change a developer environment or reduce reproducibility.

Mitigation: Prefer project-local, pinned npm tools where possible and review installation commands before running them.

Risk: Admin API examples can create, edit, delete, publish, or upload content on a Ghost site.

Mitigation: Use localhost or staging for examples, confirm before running write operations, and review payloads before applying them to production.

Risk: API examples require secrets such as Ghost Admin API keys.

Mitigation: Do not place real secrets directly into command-line examples or client-side code; use server-side handling and environment variables.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/themeix/skills/openclaw-ghost-cms)
- [Ghost Documentation](https://ghost.org/docs/)
- [Ghost Theme Development](https://ghost.org/docs/themes/)
- [Ghost CLI Documentation](https://ghost.org/docs/ghost-cli/)
- [Ghost Content API](https://ghost.org/docs/content-api/)
- [Ghost Admin API](https://ghost.org/docs/admin-api/)
- [GScan Theme Validator](https://gscan.ghost.org/)
- [Ghost Complete API Reference](https://docs.ghost.org/llms-full.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with fenced code blocks, shell commands, JSON and YAML configuration snippets, and API examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include install, validation, publishing, or Admin API examples that should be reviewed before execution against a real Ghost site.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
