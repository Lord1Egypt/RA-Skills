## Description: <br>
After an OpenClaw version bump, this skill fixes issues reported by post-update-awareness by syncing drifted plugins, restarting the gateway, verifying channel health, and preparing or applying stale openclaw.json cleanup with dry-run defaults. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hussein1362](https://clawhub.ai/user/hussein1362) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill in attended maintenance sessions after post-update-awareness reports drifted plugins or stale configuration. It proposes dry-run remediation first, then can apply plugin updates, stale openclaw.json cleanup, gateway restarts, backups, restores, and channel-health checks when explicitly confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change local OpenClaw state, including plugin versions, gateway runtime state, and openclaw.json entries. <br>
Mitigation: Review dry-run output before using --apply; every mutation is gated, creates a backup, and restores the backup if the gateway becomes unhealthy. <br>
Risk: OpenClaw config backups, logs, snapshots, and run records may contain sensitive local configuration. <br>
Mitigation: Keep generated files under the local OpenClaw profile protected and avoid sharing maintenance logs or backups without review. <br>
Risk: The skill depends on post-update-awareness for drift detection, so stale or untrusted dependency behavior could affect remediation decisions. <br>
Mitigation: Keep post-update-awareness trusted and up to date before running maintenance. <br>


## Reference(s): <br>
- [Post Update Awareness dependency](https://clawhub.ai/skills/post-update-awareness) <br>
- [RFC 6902 JSON Patch](https://datatracker.ietf.org/doc/html/rfc6902) <br>
- [Post Update Maintenance ClawHub page](https://clawhub.ai/hussein1362/post-update-maintenance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise Markdown status summaries with shell commands, JSON patch previews, backup paths, restore status, and run-record locations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; mutating actions require --apply or explicit confirmation, and run records are written under the OpenClaw profile maintenance directory.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
