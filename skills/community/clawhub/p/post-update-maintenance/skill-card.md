## Description:

After an OpenClaw version bump, this skill helps an agent sync drifted externalized plugins, restart the gateway, verify channel health, and propose or apply stale openclaw.json cleanup with mutations gated by dry-run, --apply, or explicit confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hussein1362](https://clawhub.ai/user/hussein1362)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill after OpenClaw updates to resolve drifted plugins or stale configuration reported by post-update-awareness while preserving backups and checking gateway and channel health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update OpenClaw plugins, rewrite openclaw.json, restart the gateway, and keep persistent backups and logs.

Mitigation: Run dry-run first and use --apply only during an attended maintenance window after reviewing the proposed commands and JSON patch.

Risk: High-impact local config and plugin changes rely on local execution and file-write paths.

Mitigation: Run only in a trusted OpenClaw profile directory that is not writable by other users, and preserve the generated backups for rollback.

Risk: The skill depends on post-update-awareness for drift detection.

Mitigation: Verify post-update-awareness is installed from a trusted location at a compatible version before applying maintenance changes.

Risk: Gateway or channel health can regress after plugin sync or stale-config cleanup.

Mitigation: Use the preflight backup and channel snapshots, review the post-run health diff, and restore the backup if the gateway is unhealthy after restart.

## Reference(s):

- [Post Update Maintenance on ClawHub](https://clawhub.ai/hussein1362/skills/post-update-maintenance)
- [Post Update Awareness](https://clawhub.ai/skills/post-update-awareness)
- [RFC 6902 JSON Patch](https://datatracker.ietf.org/doc/html/rfc6902)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown or plain text summaries with inline shell commands, JSON patches, and JSON run records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; mutating operations require --apply or explicit confirmation.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
