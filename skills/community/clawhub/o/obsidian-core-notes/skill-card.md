## Description: <br>
Maintain Obsidian vault core-file notes, topic synthesis notes, folder indexes, and graph links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[debtvc2022](https://clawhub.ai/user/debtvc2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and vault maintainers use this skill to scan Obsidian-style workspaces, create or refresh generated core-file sidecars and folder indexes, identify topic-synthesis candidates, and validate generated note markers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate or update local Markdown sidecars and index files across a vault. <br>
Mitigation: Run scans or refreshes on a specific vault root, review generated Markdown before relying on it, and validate marker counts after bulk operations. <br>
Risk: Cleanup can delete marker-bearing generated notes. <br>
Mitigation: Use clean-generated only when explicitly requested, prefer dry-run review first, and back up generated notes before aggressive cleanup. <br>
Risk: Vault scans and generated previews may expose private business material or secrets present under the selected root. <br>
Mitigation: Avoid scanning roots that contain sensitive material unless generated Markdown previews are acceptable for that workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/debtvc2022/obsidian-core-notes) <br>
- [Core File Rules](artifact/references/core-file-rules.md) <br>
- [Obsidian Linking Conventions](artifact/references/obsidian-linking.md) <br>
- [Topic Synthesis Core Notes](artifact/references/topic-synthesis-core-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown notes and indexes, JSON scan or candidate reports, and shell commands for local vault maintenance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files use explicit marker comments so refresh and cleanup operations can distinguish generated notes from hand-written Markdown.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
