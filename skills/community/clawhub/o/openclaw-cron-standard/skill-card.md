## Description:

Standardize OpenClaw cron wrappers, prompt contracts, and delivery-mode expectations for jobs that use ClankerHive claims, result JSON artifacts, cron delivery status, wrapper scripts, or reply-vs-message delivery behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfrederiksen](https://clawhub.ai/user/pfrederiksen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit or update OpenClaw cron jobs so wrapper behavior, result artifacts, prompt handling, and delivery.mode settings stay aligned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposed cron prompt or delivery.mode edits can change whether a scheduled job notifies users or remains silent.

Mitigation: Review delivery.mode changes against the job's actual delivery contract before applying them.

Risk: Cron contract drift can cause stale result artifacts, duplicate-run confusion, or silent not-delivered runs.

Mitigation: Apply the audit checklist and validate wrapper, prompt, claim sentinel, result artifact, and delivery.mode behavior together.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pfrederiksen/skills/openclaw-cron-standard)
- [Publisher profile](https://clawhub.ai/user/pfrederiksen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only guidance; no installer, network behavior, binaries, or auto-update behavior were identified in release security evidence.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
