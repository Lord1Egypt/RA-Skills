## Description:

Copies PikPak folders to a local disk after a dry-run review, records a backup manifest with local SHA-256 hashes, and refuses to overwrite existing files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

PikPak users use this skill to review a folder listing, then copy selected cloud files into a new local directory with a manifest for later reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live dry run reads the selected PikPak folder, and downloads use connected-app transfer quota.

Mitigation: Review the planned files and available quota before approving downloads; use a fixture with --dry-run for fully offline review.

Risk: The local SHA-256 hash does not establish that downloaded bytes match remote content.

Mitigation: Treat the manifest hash as a local reference only; the release provides size-only verification.

Risk: The manifest contains file names and paths, and the tool cannot resume or incrementally update a prior copy.

Mitigation: Protect the manifest and use a fresh destination for each run.

## Reference(s):

- [Upstream design and implementation boundaries](references/upstream-design.md)
- [PikPak connected-app transfer limits](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)
- [PikPak connected-app quota](https://mypikpak.com/zh-CN/help-center/transfer_quota/connected_apps_quota)
- [ClawHub release page](https://clawhub.ai/pipiguai87-alt/skills/pikpak-batch-backup)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [Local folder tree and backup_manifest.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The manifest records file IDs, paths, sizes, statuses, and local SHA-256 hashes; content verification is size-only.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
