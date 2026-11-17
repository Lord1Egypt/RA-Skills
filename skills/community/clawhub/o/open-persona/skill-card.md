## Description:

Meta-skill for building and managing agent persona skill packs (instruction-only; no bundled installer or auto-downloaded binaries).

This skill is ready for commercial/non-commercial use.

## Publisher:

[neiljo-gy](https://clawhub.ai/user/neiljo-gy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create, install, manage, and publish persona skill packs, including persona.json configuration, persona state integration, and explicit CLI-driven registry workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable package-manager and persona-management commands can change installed personas, skills, and local runner identity files.

Mitigation: Require explicit approval before install, update, switch, publish, register, or contribution commands; prefer pinned CLI versions and review generated persona packs and identity-file changes before activation.

Risk: Persona or skill sources selected by the user may be untrusted.

Mitigation: Install only trusted sources, review generated packs and external skill sources before use, and avoid inline curator tokens.

Risk: Generated persona packs or helper scripts may be inappropriate for sensitive environments without review.

Mitigation: Review generated code, configuration, security guidance, and scanner results before deployment in high-assurance or regulated settings.

## Reference(s):

- [OpenPersona Repository](https://github.com/acnlabs/OpenPersona)
- [Open Persona ClawHub Page](https://clawhub.ai/neiljo-gy/skills/open-persona)
- [OpenPersona Architecture Reference](references/ARCHITECTURE.md)
- [Persona Presets](references/PRESETS.md)
- [Soul Evolution Reference](references/EVOLUTION.md)
- [Faculty Reference](references/FACULTIES.md)
- [Economy & Vitality](references/ECONOMY.md)
- [Avatar Faculty Reference](references/AVATAR.md)
- [Heartbeat - Proactive Real-Data Check-ins](references/HEARTBEAT.md)
- [Persona Harvest - Community Contribution](references/CONTRIBUTE.md)
- [ACN Skill Reference](https://github.com/acnlabs/ACN/blob/main/skills/acn/SKILL.md)
- [OpenPersona Skills Directory](https://openpersona.co/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with JSON snippets, shell command blocks, and generated persona or skill-pack files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or create persona.json, SKILL.md, and related persona-pack files; install, update, switch, publish, register, and contribution actions should remain explicit user-initiated CLI commands.]

## Skill Version(s):

0.22.0 (source: ClawHub release evidence, metadata, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
