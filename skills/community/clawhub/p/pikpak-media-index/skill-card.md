## Description:

Index a PikPak media library into a searchable list with duration, resolution and codec from the CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to build a searchable inventory of video files in an authorized PikPak account. It helps review available duration, resolution, codec, size, path, and sanitized source metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports include private names and paths, and sanitized source identifiers can remain sensitive.

Mitigation: Keep reports private and select a specific folder when a whole-library scan is unnecessary.

Risk: Live compatibility with the PikPak CLI raw listing schema is not established by offline fixtures.

Mitigation: Use a trusted PikPak CLI and review the resulting inventory before relying on it.

## Reference(s):

- [Upstream field and metadata design notes](references/upstream-design.md)
- [PikPak connected-app transfer quota](https://mypikpak.com/zh-CN/help-center/transfer_quota/connected_apps_quota)
- [PikPak connected-app speed limits](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)
- [rclone PikPak file and media field definitions](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/api/types.go#L188-L280)

## Skill Output:

**Output Type(s):** [Markdown, CSV]

**Output Format:** [Searchable media inventory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Candidate metadata snapshot; scalar fields only, with sanitized source values.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
