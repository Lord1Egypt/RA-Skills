## Description:

Searches and recommends Minecraft Java Edition mods across local quick-reference data, Modrinth, optional CurseForge, and mcmod.cn, including version, loader, dependency, and compatibility guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masterhesse](https://clawhub.ai/user/masterhesse)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find Minecraft Java Edition mods, compare loader and version support, analyze modpack concepts, and identify dependency or compatibility issues before installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CurseForge API keys may be exposed if stored in a reference file or passed directly on the command line.

Mitigation: Use a protected secret store or a carefully managed environment variable for the CurseForge API key, and avoid committing keys to skill files.

Risk: Search terms may be sent to external services including Modrinth, CurseForge when configured, and mcmod.cn.

Mitigation: Avoid entering sensitive or private information in mod search queries, and review network access expectations before enabling the skill.

## Reference(s):

- [Minecraft Mod Search Skill Page](https://clawhub.ai/masterhesse/skills/minecraft-mod-search)
- [Modrinth API Reference](artifact/references/modrinth_api.md)
- [CurseForge API Reference](artifact/references/curseforge_api.md)
- [Minecraft Java Edition Version Compatibility Reference](artifact/references/mc_versions.md)
- [Minecraft Java Mod Compatibility Matrix](artifact/references/mod_compat.md)
- [Minecraft Mod Quick Reference](artifact/references/mod_quickref.md)
- [Modrinth API Documentation](https://docs.modrinth.com/api-specification/)
- [CurseForge API Documentation](https://docs.curseforge.com/)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown or JSON search results with mod recommendation cards, compatibility notes, dependency notes, and optional shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact Modrinth, CurseForge when an API key is configured, and mcmod.cn using user search terms; also uses local reference data before network search.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
