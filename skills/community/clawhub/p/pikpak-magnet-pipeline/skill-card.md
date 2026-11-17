## Description:

Run a four-step PikPak workflow to submit a magnet link, check its task, download one file, and record a receipt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use this skill with their own authorized PikPak account to submit a user-approved resource link, check task completion, download a single file, and review a cleanup command before separately deciding whether to run it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An untrusted CLI, executable path, or inherited environment could affect account operations.

Mitigation: Use a trusted CLI and an environment controlled by the operator, with an authorized account.

Risk: A failed download may leave a partial file, and a local SHA-256 receipt does not establish that content matches its source.

Mitigation: Keep receipts private, inspect the downloaded file and verify its source before separately approving any cloud deletion.

Risk: A cleanup preview could be mistaken for deletion or approval to delete the cloud item.

Mitigation: Treat it as a preview only; confirm the current account and cloud item, then make any deletion decision separately.

Risk: The real PikPak CLI account and task response schema has not been validated against a live account.

Mitigation: Stop if stable account identifiers or expected task and file fields are missing or conflict; do not guess or bypass the checks.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/pipiguai87-alt/skills/pikpak-magnet-pipeline)
- [PikPak connected-app quota](https://mypikpak.com/zh-CN/help-center/transfer_quota/connected_apps_quota)
- [PikPak connected-app speed limits](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)
- [Implementation notes and verification limits](artifact/references/upstream-design.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Files]

**Output Format:** [Chinese-first Markdown guidance, shell commands, and a JSON state receipt; downloaded content is saved as a local file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One resource per state file; single-file downloads; machine-readable output and exit codes are language-independent.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
