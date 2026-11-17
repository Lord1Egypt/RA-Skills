## Description:

Diagnoses OpenClaw "All models failed" errors caused by invalid model IDs, provider mismatches, and session fallback issues, with optional auto-repair.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:


## Use Case:

Developers and operators maintaining OpenClaw use this skill to diagnose model failover failures, preview repair actions, and optionally apply backed-up fixes to routing and session state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic fixes can persistently rewrite OpenClaw model routing to hard-coded providers and models.

Mitigation: Run diagnosis or --dry-run first, inspect every proposed routing change, and use --fix only when the named providers and models match the deployment.

Risk: Using --fix --restart can restart the OpenClaw gateway after configuration changes.

Mitigation: Use --fix without --restart when a manual or scheduled restart is preferred, and confirm that service interruption is acceptable before restarting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/halfmoon82/skills/model-failover-doctor)
- [Artifact README](artifact/README.md)
- [Artifact Skill Instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text diagnostic report with optional shell-command guidance and configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports diagnosis-only mode, dry-run preview, timestamped backups before automatic fixes, and optional OpenClaw gateway restart.]

## Skill Version(s):

1.0.0 (source: evidence release and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
