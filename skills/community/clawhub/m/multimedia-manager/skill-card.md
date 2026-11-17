## Description:

Self-hosted agent for organizing, searching, and browsing local images and videos with deduplication, full-text search, albums, favorites, CLI tools, and a localhost web gallery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nuoguo](https://clawhub.ai/user/nuoguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and self-hosting users use this skill to import, organize, search, and browse local image and video libraries through CLI tools and a localhost web gallery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The web gallery and file-serving paths could expose files beyond user expectations.

Mitigation: Use a strong IMAGE_VAULT_TOKEN, keep IMAGE_VAULT_HOST bound to 127.0.0.1, and treat original file paths as sensitive until auth and path-validation issues are fixed.

Risk: Cleanup or deletion workflows could remove more files than intended.

Mitigation: Do not run cleanup_inbound.py against arbitrary directories, review deletion targets before use, and keep backups of the local vault and SQLite database.

Risk: Imported category, tag, GPS, and location metadata may be sensitive or unsafe to display.

Mitigation: Avoid importing untrusted category or tag metadata and treat GPS/location metadata as sensitive until XSS and metadata-handling concerns are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nuoguo/skills/multimedia-manager)
- [Skill documentation](artifact/SKILL.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-capable CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local media files, thumbnails, SQLite metadata, albums, favorites, and localhost web gallery responses.]

## Skill Version(s):

1.0.6 (source: server release metadata and artifact CHANGELOG, released 2026-03-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
