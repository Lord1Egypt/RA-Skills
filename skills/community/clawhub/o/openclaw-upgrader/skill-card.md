## Description:

Upgrade OpenClaw to a specific version or latest using a cross-platform, Codex-supervised flow. Use when the user asks to upgrade or update OpenClaw. OpenClaw should do lightweight pre-upgrade preparation itself, then hand the full upgrade, restart, recovery, service-definition refresh, and verification workflow to Codex with a strong prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gejiliang](https://clawhub.ai/user/gejiliang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate same-host OpenClaw upgrades through a local coding agent while preserving instance identity, service recovery, endpoint verification, and structured upgrade results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change a live OpenClaw installation, restart or repair services, and write files under the OpenClaw user area.

Mitigation: Review the generated upgrade plan, confirm backups and target instance identity, and require explicit approval before package or service changes.

Risk: The flow can contact Codex or Claude Code during preflight and delegated upgrade execution.

Mitigation: Require explicit user confirmation before external agent preflights or delegation, and record the selected agent and preflight outcome.

Risk: Server security guidance identifies result-path Python injection, lock cleanup, and delegate command selection as areas needing hardening.

Mitigation: Review and remediate those issues before broad deployment; restrict delegate commands to trusted configured paths and use safe result paths.

Risk: Concurrent upgrade runs or incorrect lock ownership can leave the host in an inconsistent upgrade state.

Mitigation: Verify that the host-level lock covers the full upgrader lifecycle and that terminal cleanup only releases locks owned by the active run.

## Reference(s):

- [OpenClaw Upgrader Review Checklist](references/review-checklist.md)
- [OpenClaw Upgrader ClawHub Page](https://clawhub.ai/gejiliang/skills/openclaw-upgrader)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON files]

**Output Format:** [Markdown guidance with shell commands and structured JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces context and result JSON for a same-host OpenClaw upgrade flow.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
