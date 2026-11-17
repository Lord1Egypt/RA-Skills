## Description:

Generate a daily health brief from Oura, Whoop, and Withings with unified re-auth, local token persistence, and a Green/Yellow/Red morning summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nathanielweiner](https://clawhub.ai/user/nathanielweiner)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to connect WHOOP, Oura, and Withings accounts, normalize daily sleep, activity, and body metrics, and produce a concise morning health brief for review or scheduled delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive health-provider data and long-lived OAuth refresh tokens.

Mitigation: Use a narrow 1Password vault or dedicated environment file containing only the required provider credentials, and restrict access to generated health outputs.

Risk: Local token persistence can expose refreshed OAuth tokens if the local secrets file is readable by unintended users.

Mitigation: Keep ~/.openclaw/secrets/health_tokens.json permission-restricted, monitor file access, and rotate or revoke provider tokens if exposure is suspected.

Risk: Scheduled runs may receive broader credentials than needed if they source a general environment file.

Mitigation: Provide cron with the smallest credential set needed for WHOOP, Oura, Withings, and the selected delivery channel.

## Reference(s):

- [OpenClaw Health Brief ClawHub listing](https://clawhub.ai/nathanielweiner/skills/openclaw-health-brief)
- [Morning Brief Format](docs/MORNING_BRIEF.md)
- [1Password Conventions](docs/1PASSWORD_CONVENTIONS.md)
- [Oura Provider Notes](docs/OURA.md)
- [WHOOP Provider Notes](docs/WHOOP.md)
- [Withings Provider Notes](docs/WITHINGS.md)
- [OpenClaw Cron Documentation](https://docs.openclaw.ai/automation/cron)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration]

**Output Format:** [Normalized JSON file plus Markdown morning brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contains personal health metrics from configured providers; unavailable metrics are represented as null.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
