## Description:

Deprecated and renamed to `miab-observer`, `interagent-queue` observes the MIAB transaction ledger, renders callback events to human-readable logs, and can post closed-bottle summaries to a configured chat target.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albzhu](https://clawhub.ai/user/albzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor a `miab-broker` callback ledger, maintain readable transaction logs, and optionally send completed task summaries to a configured chat destination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional closed-bottle notifier can resend historical task details if `closed_bottle_state.json` is corrupted or reset.

Mitigation: Prefer the renamed `miab-observer` release when available, review dry-run output first, and avoid cron delivery until state recovery and ledger-rotation handling are operationally defined.

Risk: Closed-bottle summaries may be posted to the configured Discord or chat target.

Mitigation: Set `CLAW_CLOSED_TARGET` deliberately, verify the destination before enabling the notifier, and use the dry-run script to inspect message content before delivery.

Risk: The deprecated skill name will not automatically migrate existing installs to `miab-observer`.

Mitigation: Install `miab-observer`, update cron command paths from `interagent_queue.py` to the renamed script, confirm shared state paths, and then remove `interagent-queue`.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albzhu/skills/interagent-queue)
- [SKILL.md](artifact/SKILL.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline bash commands; runtime scripts emit plain text logs and JSON status or dry-run output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The default observer writes local log and cursor files; the optional notifier delegates delivery to `openclaw message send` using the configured target.]

## Skill Version(s):

1.3.0 (source: server release metadata and CHANGELOG; released 2026-08-28; final interagent-queue release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
