## Description:

OpenClaw Soul Weaver generates personalized OpenClaw agent configuration files from conversational inputs, celebrity or profession templates, and optional avatar settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[addogiavara-tech](https://clawhub.ai/user/addogiavara-tech)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to create personalized agent configuration bundles for assistants with selected identities, memories, tools, and execution guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends provided name, profession, use case, style, persona, and avatar prompt data to an external service.

Mitigation: Avoid sensitive profile details unless the external service is approved for the intended use.

Risk: Generated SOUL.md, MEMORY.md, TOOLS.md, and AGENTS.md files can shape future agent behavior.

Mitigation: Review every generated configuration file before applying it to an agent workspace.

Risk: The evidence flags broad triggers and inconsistent file permissions.

Mitigation: Use only the permissions needed for the intended workflow and review generated file paths before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/addogiavara-tech/skills/openclaw-soul-weaver)
- [Publisher profile](https://clawhub.ai/user/addogiavara-tech)
- [Template reference](references/templates.md)
- [Tool configuration reference](references/tools.md)
- [Online creation service](https://sora2.wboke.com/)
- [Generation API endpoint](https://sora2.wboke.com/api/v1/generate)
- [Image generation endpoint](https://sora2.wboke.com/api/generate-image)

## Skill Output:

**Output Type(s):** [markdown, configuration, code, shell commands, guidance]

**Output Format:** [Markdown configuration files and a ZIP package]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates SOUL.md, IDENTITY.md, MEMORY.md, USER.md, TOOLS.md, AGENTS.md, and optional avatar path metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, CHANGELOG, released 2026-03-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
