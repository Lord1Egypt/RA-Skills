## Description:

Create and customize AI personas with voice, visual identity, personality, memory, and cross-platform behavior using an interactive wizard and safe update tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spfadvisors](https://clawhub.ai/user/spfadvisors)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create, update, preview, validate, migrate, import, and export persistent AI persona workspaces with generated persona files and configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted .persona bundles may write more workspace content than users expect during import.

Mitigation: Import bundles only from trusted sources, inspect bundle contents before use, and avoid --force so existing files are not overwritten without review.

Risk: Exported bundles can include personal context, memory files, and voice configuration.

Mitigation: Review USER.md, MEMORY.md, memory directories, and voice settings before sharing any exported bundle.

Risk: Update and regeneration flows can alter persona files, especially when confirmation is bypassed.

Mitigation: Use dry-run, preview, diff, backup, and validation workflows before applying changes; reserve force options for reviewed changes.

## Reference(s):

- [AI Persona Engine Skill Page](https://clawhub.ai/spfadvisors/skills/persona-engine)
- [Config Schema Reference](references/config-schema.md)
- [Voice Providers Guide](references/voice-providers.md)
- [Image Providers Guide](references/image-providers.md)
- [Personality Archetypes](references/personality-archetypes.md)
- [SOUL.md Writing Guide](references/soul-writing-guide.md)
- [Migration Guide](references/migration-guide.md)
- [Design Document](DESIGN.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, JSON configuration, shell command guidance, and portable persona bundles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate SOUL.md, USER.md, IDENTITY.md, MEMORY.md, AGENTS.md, HEARTBEAT.md, openclaw.json updates, previews, diffs, validation reports, and .persona bundles.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
