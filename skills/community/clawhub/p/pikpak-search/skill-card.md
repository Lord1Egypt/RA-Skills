## Description:

Search a PikPak drive by filename when the official CLI has no search command, returning a bounded result list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

PikPak account holders can search authorized drive listings by filename when their CLI lacks a search command. They can filter and sort bounded results, then optionally save a local report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved reports contain private filenames and paths.

Mitigation: Keep reports private and choose the output location deliberately.

Risk: Complex regular expressions can consume excessive time because Python regular expressions have no runtime limit.

Mitigation: Prefer ordinary text searches; only use simple, trusted regular expressions.

Risk: Live PikPak CLI compatibility and large-library behavior remain unverified.

Mitigation: Use a trusted, authenticated PikPak CLI and restrict searches to a folder when practical.

## Reference(s):

- [Upstream design review and implementation limits](artifact/references/upstream-design.md)
- [PikPak connected-app speed limits](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)
- [PikPak connected-app transfer quota](https://mypikpak.com/zh-CN/help-center/transfer_quota/connected_apps_quota)
- [rclone PikPak listing design reference](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/pikpak.go#L769-L823)
- [pikpakcli listing design reference](https://github.com/52funny/pikpakcli/blob/560f263661fc55e40e508fe8e0d4b151c855dcbd/cli/list/list.go)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [Text or JSON search results, with an optional local report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a bounded result list; reports can contain private filenames and paths.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
