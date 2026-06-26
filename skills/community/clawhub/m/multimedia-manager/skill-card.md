## Description: <br>
Self-hosted agent to organize, search, and browse images and videos with auto-deduplication, full-text search, albums, favorites, and a responsive web gallery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nuoguo](https://clawhub.ai/user/nuoguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local users use this skill to set up and operate a self-hosted media vault for importing, deduplicating, searching, organizing, and browsing images and videos on their own machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The gallery indexes private media and may store sensitive metadata such as precise photo locations. <br>
Mitigation: Keep the vault and database local, restrict file permissions, and review stored metadata before sharing exports or backups. <br>
Risk: The gallery can run without authentication if IMAGE_VAULT_TOKEN is not configured. <br>
Mitigation: Run setup to generate a token, keep the .env file and terminal output private, and confirm the token is set before serving the gallery. <br>
Risk: Binding IMAGE_VAULT_HOST to a public interface can expose the local gallery. <br>
Mitigation: Keep the default localhost binding unless the deployment has hardened authentication and network controls. <br>
Risk: The cleanup script deletes inbound files using an hours-based threshold. <br>
Mitigation: Use --dry-run first, confirm the target directory, and set the threshold deliberately before deleting files. <br>


## Reference(s): <br>
- [Multimedia Manager ClawHub Release](https://clawhub.ai/nuoguo/multimedia-manager) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local file operations, SQLite-backed media indexing, and optional JSON output from CLI search commands.] <br>

## Skill Version(s): <br>
1.0.6 (source: release evidence and changelog, released 2026-03-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
