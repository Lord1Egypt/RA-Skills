## Description:

Verify OpenClaw after upgrades against an operator-maintained model, cron, and channel ground truth. Use for report-only config integrity, provider liveness, cron integrity, session smoke tests, and channel checks; require explicit approval before applying repairs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathanjing](https://clawhub.ai/user/jonathanjing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill after OpenClaw upgrades or during periodic health checks to compare runtime configuration, recurring cron jobs, model liveness, sessions, and channels against maintained ground truth. It produces reports by default and requires explicit operator approval before bounded config or cron repairs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access full OpenClaw runtime configuration, which may include secrets.

Mitigation: Prefer metadata-only config access where available and follow the documented zero-secret logging behavior for redaction, sensitive drift reporting, and no credential persistence.

Risk: The skill can send liveness test messages to configured channels.

Mitigation: Use dedicated ops or test channels for liveness checks and review channel targets before running verification.

Risk: The skill can propose config and cron repairs that change runtime behavior.

Mitigation: Keep runs report-only until an operator reviews the redacted repair plan and explicitly approves each bounded change.

Risk: Upgrade verification depends on the installed OpenClaw and skill versions.

Mitigation: Pin OpenClaw or skill versions for production upgrade workflows when repeatability is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jonathanjing/skills/ground-control)
- [ClawHub homepage metadata](https://clawhub.ai/jonathanjing/ground-control)
- [Ground truth template](artifact/templates/MODEL_GROUND_TRUTH.md)
- [Post-upgrade verification prompt](artifact/scripts/post-upgrade-verify.md)
- [Upgrade SOP](artifact/scripts/UPGRADE_SOP.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown verification reports with inline command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report-only by default; bounded config and cron repair steps require explicit operator approval.]

## Skill Version(s):

0.3.6 (source: server release metadata, SKILL.md metadata, CHANGELOG released 2026-08-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
