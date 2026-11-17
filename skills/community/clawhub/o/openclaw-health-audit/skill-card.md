## Description:

OpenClaw system health audit and auto-repair skill for monitoring prompt size, cron compliance, session cleanup, and token usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators maintaining OpenClaw instances use this skill to generate health reports, audit prompt, cron, session, cache, and token-cost issues, and run guided repairs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a recurring health-check cron job and make persistent changes to local OpenClaw cron and session state.

Mitigation: Review generated reports before applying fixes, keep backups of cron and session state files, and run targeted repairs before using --fix all.

Risk: Broad repair commands may change more OpenClaw state than a user expects.

Mitigation: Manually verify proposed provider, model routing, cron, and session changes before authorizing repair commands.

## Reference(s):

- [OpenClaw Token Economy Audit Methodology](references/layer-audit-guide.md)
- [ClawHub skill homepage](https://clawhub.ai/halfmoon82/openclaw-health-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown health reports with shell commands and optional JSON-backed configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local OpenClaw cron and session state when the user runs repair commands.]

## Skill Version(s):

1.5.0 (source: server release metadata; artifact files contain older 1.0.0 and 1.4.0 version references)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
