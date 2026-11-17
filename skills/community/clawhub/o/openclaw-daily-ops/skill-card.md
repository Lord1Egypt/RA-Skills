## Description:

Daily cost reporting + session hygiene for OpenClaw deployments. Tracks per-session API spend, shows 7-day trend, and wipes zombie sessions >24h old to prevent context snowball. Zero personal info -- configure with your own paths and Discord channel. Runs nightly via cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zylcold](https://clawhub.ai/user/zylcold)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor daily OpenClaw API spend, post concise Discord cost reports, and reset stale high-context sessions during scheduled operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can permanently truncate stale session files.

Mitigation: Run dry-run first, execute under an unprivileged account, and confirm configured session paths before enabling scheduled resets.

Risk: Usage summaries can be sent to an external Discord webhook.

Mitigation: Restrict access to the configuration file and review what session names or usage metadata may appear in reports.

Risk: Weak path safeguards could affect files outside the intended sessions directory if configuration or metadata is wrong.

Mitigation: Validate that sessionFile paths remain inside the configured sessions directory before running the reset script.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zylcold/skills/openclaw-daily-ops)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report text with inline shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write local JSON state logs and post usage summaries to a configured Discord webhook.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
