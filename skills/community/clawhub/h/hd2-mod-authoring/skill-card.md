## Description:

Guides agents through authoring, installing, and troubleshooting Helldivers 2 mods, including patch packaging, conflict checks, and game-log verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cavadus](https://clawhub.ai/user/cavadus)

### License/Terms of Use:

MIT

## Use Case:

Helldivers 2 mod developers use this skill to classify installed patches, identify conflicting changes, author and package mods, and verify behavior using logs and read-only diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory patches can crash the game or corrupt game state if offsets or target values are wrong.

Mitigation: Back up files, confirm the target is your own game process, verify current offsets and values before writing, and read back changes.

Risk: Mod deployment can overwrite files or conflict with other installed patches.

Mitigation: Confirm the target path, close the mod manager, check for competing value writers, and retain a rollback copy.

Risk: Diagnostic memory dumps may expose sensitive process data.

Mitigation: Restrict access to dump files and securely remove them when no longer needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cavadus/skills/hd2-mod-authoring)
- [Project homepage listed in skill metadata](https://github.com/Cavadus/hd2-mod-authoring)
- [Install and patch format reference](references/install-and-format.md)
- [Memory census and diagnostic reference](references/memory-census.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code and commands; mod source and deployment files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Game-memory offsets and patch layouts require verification against the installed game build.]

## Skill Version(s):

0.1.8 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
