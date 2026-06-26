## Description: <br>
Create, inspect, and restore versioned OpenClaw state backups with rollback safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Danielwangyy](https://clawhub.ai/user/Danielwangyy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create restorable snapshots, inspect backup manifests, verify archives, preview restore plans, and recover OpenClaw memory, workspace, session, and configuration state after migration or breakage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may include private memory, session metadata, configuration, and local skills. <br>
Mitigation: Store backup archives in trusted locations, restrict access to generated tar.gz and manifest files, and review backup scope before sharing or migrating archives. <br>
Risk: The security scan reports that restore_state.py can unsafely unpack crafted archives before validation. <br>
Mitigation: Do not restore archives from other people or uncertain sources; use verify-only review first and require archive member validation that rejects path traversal, absolute paths, links, devices, and unexpected manifest paths before extraction. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Danielwangyy/openclaw-state-backup) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and references to generated JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled scripts create tar.gz backup archives, manifest.json files, checksum metadata, and restore or dry-run JSON reports.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
