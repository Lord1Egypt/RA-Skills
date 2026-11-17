## Description:

Safe configuration file editing for JSON, YAML, TOML, and other config formats. Use when working with configuration files for: (1) Reading config values, (2) Updating/adding/removing keys, (3) Creating new config files, (4) Validating syntax, (5) Merging configs, (6) Converting between formats, or (7) Debugging config issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dougchambes](https://clawhub.ai/user/dougchambes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to safely inspect, edit, validate, merge, convert, and troubleshoot configuration files while preserving syntax and reducing accidental damage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad global installation examples may install unverified or unexpectedly changing tooling.

Mitigation: Review installation commands before execution; prefer already installed tools, pinned versions, checksums or signatures, and user-local or virtual-environment installs.

Risk: Configuration edits can break application behavior or lose existing settings.

Mitigation: Back up the target file first, use format-aware tools, validate syntax after edits, and test the changed configuration in the application context.

## Reference(s):

- [Configuration Formats Reference](references/formats.md)
- [ClawHub Skill Page](https://clawhub.ai/dougchambes/skills/legend-config-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file-editing recommendations, validation commands, format conversion steps, and backup guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
