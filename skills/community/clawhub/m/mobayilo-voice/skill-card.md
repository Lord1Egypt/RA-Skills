## Description:

Place outbound phone calls via Mobayilo with safe defaults (preview mode by default) and explicit live execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adusingi](https://clawhub.ai/user/adusingi)

### License/Terms of Use:


## Use Case:

Developers and workflow operators use this skill when an OpenClaw workflow needs a guarded outbound phone call step for booking, confirmation, or follow-up. It supports readiness checks, preview-mode call preparation, and explicitly enabled live calling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real outbound phone calls when live execution is enabled.

Mitigation: Keep preview mode as the default, require explicit --execute for live calls, and use approval gates when workflows need human confirmation.

Risk: Installation and update guidance relies on trusted local code execution paths, including curl|sh and self-update behavior.

Mitigation: Use pinned, verified Mobayilo CLI releases before production deployment.

Risk: Status and telemetry handling may expose account details or operational metadata.

Mitigation: Preserve phone-number masking and tighten logs and temporary files so account email, exact balances, and unrelated environment secrets are not unnecessarily exposed.

## Reference(s):

- [Mobayilo Voice ClawHub listing](https://clawhub.ai/adusingi/skills/mobayilo-voice)
- [Mobayilo homepage](https://mobayilo.com)
- [Mobayilo Voice README](README.md)
- [Mobayilo Voice Adapter Runbook](docs/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Human-facing summaries, Markdown instructions, shell commands, and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview mode is the default; live calls require explicit execution.]

## Skill Version(s):

0.2.0-beta.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
