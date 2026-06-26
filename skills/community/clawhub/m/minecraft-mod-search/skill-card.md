## Description: <br>
Searches and recommends Minecraft Java Edition mods across quick-reference data, Modrinth, CurseForge, and MC百科, with version, loader, dependency, and compatibility guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[masterhesse](https://clawhub.ai/user/masterhesse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Minecraft Java players, modpack builders, and agent users use this skill to find mods for a stated feature, compare loader and version support, and assemble compatible recommendations for modpacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may be sent to external mod services such as Modrinth, CurseForge, or MC百科. <br>
Mitigation: Avoid placing private information in mod search prompts, and confirm ambiguous requests before running network searches. <br>
Risk: CurseForge searches may require a sensitive API key. <br>
Mitigation: Prefer an environment variable or runtime argument for the key, and avoid storing it in shared files. <br>
Risk: Mod version and compatibility data can become stale or incomplete. <br>
Mitigation: Verify selected mods, loaders, dependencies, and Minecraft versions on the source platform before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/masterhesse/minecraft-mod-search) <br>
- [Modrinth API documentation](https://docs.modrinth.com/api-specification/) <br>
- [CurseForge API documentation](https://docs.curseforge.com/) <br>
- [Modrinth API reference](references/modrinth_api.md) <br>
- [CurseForge API reference](references/curseforge_api.md) <br>
- [Minecraft version reference](references/mc_versions.md) <br>
- [Mod compatibility matrix](references/mod_compat.md) <br>
- [Mod quick-reference table](references/mod_quickref.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Markdown or plain text recommendations, with optional JSON results from the bundled search script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include mod names, source links, download and version metadata, loader compatibility, dependency notes, warnings, and installation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
