## Description:

Generate a daily health brief from Oura, Whoop, and Withings with unified re-auth, local token persistence, and a Green/Yellow/Red morning summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nathanielweiner](https://clawhub.ai/user/nathanielweiner)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate daily personal health summaries from connected Oura, WHOOP, and Withings accounts. It normalizes provider data into JSON and produces a concise Markdown morning brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests and stores OAuth credentials and refresh tokens for health providers.

Mitigation: Install only after reviewing provider scopes, use the minimum scopes needed, and keep local token files and 1Password vault access private.

Risk: Health summaries and JSON outputs may contain sensitive personal health data.

Mitigation: Choose private output paths and delivery channels, and avoid sending cron summaries to channels that are not access-controlled.

Risk: Live API calls are attempted by default when credentials exist.

Mitigation: Use sample mode for offline checks or validation runs before enabling live provider access.

## Reference(s):

- [OpenClaw Health ClawHub listing](https://clawhub.ai/nathanielweiner/skills/openclaw-health)
- [OpenClaw cron documentation](https://docs.openclaw.ai/automation/cron)
- [1Password conventions](docs/1PASSWORD_CONVENTIONS.md)
- [Morning brief format](docs/MORNING_BRIEF.md)
- [Oura connector notes](docs/OURA.md)
- [WHOOP connector notes](docs/WHOOP.md)
- [Withings connector notes](docs/WITHINGS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown summary with normalized JSON files and setup shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform live health-provider API calls when credentials are configured; returns null metrics with an error block when credentials are unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
