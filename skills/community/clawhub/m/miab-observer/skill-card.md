## Description:

Observe the MIAB transaction ledger: render callback events to a human-readable log, and optionally post closed-bottle summaries to a chat target.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albzhu](https://clawhub.ai/user/albzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use MIAB Observer to inspect MIAB callback ledger activity, manage observer sweeps, and optionally send closed-bottle summaries to an approved chat target.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional notifier can send ledger task or result content to an external chat target.

Mitigation: Use the local observer by default, configure CLAW_CLOSED_TARGET only for an approved destination, and run the dry-run script before enabling delivery.

Risk: The MIAB ledger may contain secrets, internal prompts, customer data, or untrusted agent output.

Mitigation: Review ledger sensitivity before installing or enabling notifications, and avoid unattended Discord delivery until redaction and mention escaping are added.

Risk: Notifier state safety is called out as weak in the security evidence.

Mitigation: Avoid unattended delivery until fail-closed notifier state handling is added, and inspect notifier state deliberately after failures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albzhu/skills/miab-observer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; runtime scripts produce plain text logs and JSON status output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires miab-broker 2.0.0 or later and local environment configuration for ledger, state, log, registry, and optional chat delivery targets.]

## Skill Version(s):

2.0.0 (source: server release metadata and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
