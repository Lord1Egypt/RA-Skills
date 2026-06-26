## Description: <br>
Create and customize AI personas with voice, face, personality, memory, and cross-platform behavior using an interactive wizard and safe update tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spfadvisors](https://clawhub.ai/user/spfadvisors) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create, update, validate, export, and import persistent AI personas with generated workspace files, persona configuration, voice and image provider settings, and optional memory scaffolding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persona bundles and generated persona files can expose sensitive local data, especially when memory files or voice configuration are exported. <br>
Mitigation: Treat .persona bundles as untrusted, inspect exports before sharing, avoid importing bundles from unknown sources, and verify voice configuration contains no credentials before export. <br>
Risk: Import and update flows can overwrite existing local persona files or openclaw.json settings. <br>
Mitigation: Review generated files, use dry-run, diff, backup, and confirmation flows where available, and avoid force options unless the changes have been inspected. <br>
Risk: Automatic memory, voice, and image features may persist data or contact configured providers unexpectedly. <br>
Mitigation: Disable spontaneous voice/image and memory features when automatic persistence or provider use is not desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/spfadvisors/persona-engine) <br>
- [Configuration Schema Reference](references/config-schema.md) <br>
- [Voice Providers Guide](references/voice-providers.md) <br>
- [Image Providers Guide](references/image-providers.md) <br>
- [Personality Archetypes](references/personality-archetypes.md) <br>
- [SOUL.md Writing Guide](references/soul-writing-guide.md) <br>
- [Migration Guide](references/migration-guide.md) <br>
- [Design Document](DESIGN.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown workspace files, JSON configuration, .persona bundles, CLI guidance, diffs, validation reports, and preview text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update OpenClaw workspace files and openclaw.json; export and import flows can include persona memory or voice configuration when selected.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
