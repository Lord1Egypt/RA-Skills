## Description:

OpenClaw Agency Agents manages and activates AI agent personas from the agency-agents-zh collection, with commands for listing, searching, updating, restoring, and activating professional agents across engineering, design, marketing, sales, product, and other domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roymax](https://clawhub.ai/user/roymax)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to browse and activate specialized agent personas for work such as engineering, design, marketing, sales, product, legal, finance, and support tasks. The skill can replace workspace instruction files with the selected persona while keeping local backups for restoration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill pulls mutable third-party content and can place selected remote Markdown into persistent workspace instruction files.

Mitigation: Use a pinned and reviewed repository revision where possible, inspect persona content before activation or update, and install only when the agency-agents-zh source is trusted.

Risk: Activation can overwrite SOUL.md, IDENTITY.md, and AGENTS.md in the workspace.

Mitigation: Keep and review backups before activation, verify restore behavior, and confirm that replaced instruction files match the intended persona.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roymax/skills/openclaw-agency-agents)
- [agency-agents-zh repository](https://github.com/jnMetaCode/agency-agents-zh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update local workspace instruction files and backup directories when activation or restore scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
