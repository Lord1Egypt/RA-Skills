## Description:

Report PikPak folder sizes, file counts, and largest files without changing cloud files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

PikPak users use this skill to review folder sizes, file counts, and known largest files when deciding what to organize.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Omitting a folder scans the drive root, and --depth does not reduce scan coverage.

Mitigation: Confirm the authorized folder before scanning and use --folder to limit the scan scope.

Risk: Reports may contain private paths, and an existing report file can be overwritten.

Mitigation: Keep reports in a controlled private directory and choose a dedicated output file.

Risk: Live-service compatibility has not been verified.

Mitigation: Use a trusted PikPak CLI and confirm compatibility before relying on live results.

## Reference(s):

- [Upstream design and implementation notes](references/upstream-design.md)
- [PikPak connected-app quota guidance](https://mypikpak.com/zh-CN/help-center/transfer_quota/connected_apps_quota)
- [rclone structured listing reference](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/docs/content/commands/rclone_lsjson.md#L99-L118)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable storage summary and JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only cloud scan; --depth limits display only; account overview is not queried.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
