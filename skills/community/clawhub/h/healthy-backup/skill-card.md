## Description: <br>
Health-gated backup for OpenClaw rigs that audits first, backs up only if healthy, supports tiered retention and optional rclone sync, and scrubs sensitive config values before staging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LittleJakub](https://clawhub.ai/user/LittleJakub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to configure and run health-gated encrypted backups, test backup readiness with dry runs, and optionally schedule or sync backup archives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may expose sensitive material if credential files, backup roots, or optional collectors are configured carelessly. <br>
Mitigation: Run --dry-run before installing, use the smallest backup tier that meets recovery needs, keep backup.key chmod 600 and outside shared or cloud folders, and leave sensitive collectors disabled unless needed. <br>
Risk: A backup archive may not be recoverable if encryption keys or archive integrity are not checked before relying on it. <br>
Mitigation: Verify that the backup root is private and test decryption or restore of at least one archive before depending on scheduled backups. <br>
Risk: The bundled checksum block may be stale for the server release. <br>
Mitigation: Compare downloaded files against trusted package metadata rather than relying only on the checksum block in SKILL.md. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/LittleJakub/healthy-backup) <br>
- [Publisher profile](https://clawhub.ai/user/LittleJakub) <br>
- [rclone installer reference](https://rclone.org/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is intended for Linux/OpenClaw environments with tar, gpg, jq, and rsync available; rclone and Ollama are optional.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata and CHANGELOG top entry) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
