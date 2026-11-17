## Description:

Track menstrual cycle history, answer current cycle status questions, record new period start dates from natural-language messages such as "月经来了", predict the next expected start date, and prepare reminder schedules for OpenClaw users who need private menstrual health tracking with local encrypted storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjian124](https://clawhub.ai/user/wangjian124)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to privately record period start dates, check current cycle status, estimate the next start date, and prepare reminder schedules. It is intended as data-based tracking support, not medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive menstrual-health data and may place reminder details into scheduler, chat, or webhook paths in plaintext.

Mitigation: Install only with explicit user consent, prefer neutral reminder wording, restrict access to OpenClaw config, state, scheduler logs, and chat notifications, and treat reminder payloads as sensitive health data.

Risk: Webhook delivery can send health-related reminder content to external destinations.

Mitigation: Avoid webhook delivery unless destinations are administrator-approved; prefer native delivery routes or no delivery when a safe route is unavailable.

Risk: Forecasts and phase labels are estimates based on recorded start dates and may be unreliable with sparse or irregular history.

Mitigation: Tell users when confidence is low or history is sparse, avoid medical certainty, and suggest professional medical advice for severe pain, unusual bleeding, or highly irregular cycles.

## Reference(s):

- [Deployment Notes](references/deployment.md)
- [Forecast Model And Privacy](references/model-and-privacy.md)
- [OpenClaw ClawHub Documentation](https://docs.openclaw.ai/tools/clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Natural-language responses with JSON helper output, inline shell commands, and cron configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces cycle status, forecast confidence, reminder plans, and privacy guidance; helper state is local and encrypted when configured with PERIOD_TRACKER_KEY.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
