## Description:

OpenClaw Dual Cleanup helps agents inspect and clean stale OpenClaw session indexes, session files, caches, and temporary files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ltap266](https://clawhub.ai/user/ltap266)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to preview, run, or configure cleanup of accumulated OpenClaw session data and caches. It is intended for maintenance workflows where stale session files consume disk space or remain after index cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad cleanup rules may delete session, cache, or temporary files that the user still needs.

Mitigation: Run in dry-run mode first and inspect the candidate file list before allowing deletion.

Risk: Force mode bypasses interactive confirmation and increases the impact of an incorrect file match.

Mitigation: Use force mode only after validating the same command in dry-run mode with the intended age threshold.

Risk: Cron or boot-time automation can repeatedly run a destructive maintenance task without fresh review.

Mitigation: Do not enable scheduled or boot-time examples unless the cleanup scope and retention window have been reviewed.

Risk: Elevated privileges can expand deletion impact beyond the user's normal OpenClaw data.

Mitigation: Run without sudo or administrator privileges so cleanup remains limited to the user's accessible files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ltap266/skills/openclaw-dual-cleanup)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Cleanup script](artifact/scripts/clean-sessions-dual.py)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with shell command examples and cleanup reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose dry-run, interactive, or force cleanup modes before deleting local session and cache files.]

## Skill Version(s):

2.0.1 (source: server release metadata and target metadata; artifact docs include older 2.0.0 and 1.3.0 labels)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
