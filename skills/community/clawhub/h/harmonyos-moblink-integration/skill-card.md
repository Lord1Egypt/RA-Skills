## Description:

Guides agents through integrating MobTech MobLink into HarmonyOS NEXT projects, including ohpm dependency setup, privacy consent wiring, URI scheme configuration, scene restore, and mobID generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mobsupport](https://clawhub.ai/user/mobsupport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add MobTech MobLink deep-linking and scene restoration to HarmonyOS NEXT applications. The workflow helps configure project dependencies, permissions, privacy consent handling, URI scheme routing, and generated integration notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to place appSecret in a plaintext MobLink_Config.xlsx spreadsheet.

Mitigation: Use the skill only in trusted project workspaces, avoid committing MobLink_Config.xlsx, and prefer environment variables or a secret manager for appSecret.

Risk: The generated privacy sheet defaults several optional privacy-sensitive data collection settings to enabled.

Mitigation: Change optional data collection settings to opt-in values that match the application's privacy notice and user consent flow before integration.

Risk: The workflow installs third-party MobTech SDK packages from ohpm.

Mitigation: Pin and verify SDK package versions before installation and review dependency changes before release.

## Reference(s):

- [MobLink documentation entry](https://www.mob.com/wiki/detailed?wiki=661&id=34)
- [HarmonyOS NEXT integration guide](https://mob.com/wiki/detailed?wiki=731&id=34)
- [MobLink console configuration](https://mob.com/wiki/detailed?wiki=527&id=34)
- [MobLink HarmonyOS compliance guide](https://mob.com/wiki/detailed?wiki=758&id=34)
- [MobLink FAQ](https://mob.com/wiki/detailed?wiki=530&id=34)
- [MobLink privacy policy](https://mob.com/wiki/detailed?wiki=97&id=34)
- [Extended business feature settings](https://www.mob.com/wiki/detailed?wiki=730&id=34)
- [OpenHarmony ohpm registry](https://ohpm.openharmony.cn/ohpm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, TypeScript snippets, JSON5 configuration examples, and generated project documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate an Excel configuration template and a project-level MOBLINK_README.md during agent execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
