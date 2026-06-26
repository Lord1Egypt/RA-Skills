## Description: <br>
Cross-platform Obsidian sync (Mac to iPhone) powered by Syncthing, with no Obsidian plugins, offline-first operation, and large-file filtering guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ameylover](https://clawhub.ai/user/ameylover) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to configure bidirectional Obsidian vault sync between macOS and iPhone with Syncthing and Mobius Sync. It provides setup steps, troubleshooting guidance, and optional large-file filtering commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional rsync script can copy private Obsidian notes to an iCloud destination despite the guide's no-iCloud positioning. <br>
Mitigation: Review and edit all paths before use, and avoid the rsync/iCloud script unless a second copy in that destination is intentional. <br>
Risk: Following sync commands with incorrect paths could copy, omit, or overwrite notes unexpectedly. <br>
Mitigation: Back up the vault first, enable Syncthing file versioning, and verify source and destination paths before running commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ameylover/obsidian-sync-syncthing) <br>
- [English skill instructions](artifact/SKILL.en.md) <br>
- [English README](artifact/README.en.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes user-edited local file paths, device pairing steps, and optional sync filtering commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
