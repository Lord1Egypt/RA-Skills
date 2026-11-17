## Description:

JiaHeng is a Chinese-language companion persona for wb-open-builder that guides OpenClaw asset creation with field-level pre-review discipline, confirmation gates, validation reporting, and delivery refusal on failed checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and asset creators use this skill alongside wb-open-builder to plan, generate, validate, and package OpenClaw platform assets. It provides a strict pre-review persona that asks for confirmation before generation, applies checklist-driven validation, and surfaces failed checks instead of delivering non-compliant assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad file-writing and Bash authority for asset generation, validation, and packaging.

Mitigation: Run it only in workspaces where asset files may be created or modified, and review generated files and commands before using them outside that workspace.

Risk: The skill depends on wb-open-builder for authoritative platform fields, templates, and validation behavior.

Mitigation: Load it alongside wb-open-builder for full asset-generation workflows; if wb-open-builder is unavailable, use the skill only for consultation or checklist-style review.

Risk: The skill may activate on broad OpenClaw asset-building requests.

Mitigation: Confirm the intended asset type and scope before allowing generation, validation, or packaging actions.

## Reference(s):

- [Character Data](references/character-data.md)
- [Character Requirements](references/character-requirements.md)
- [Dialogue Examples](references/dialogue.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and structured text, with code blocks or shell commands when generating, validating, or packaging assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese-language, checklist-driven interaction, validation summaries, file edits, and packaging guidance for OpenClaw asset workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
