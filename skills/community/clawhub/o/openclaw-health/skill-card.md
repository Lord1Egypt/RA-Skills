## Description: <br>
Generate a daily health brief from Oura, Whoop, and Withings with unified re-authentication, local token persistence, and a Green/Yellow/Red morning summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NathanielWeiner](https://clawhub.ai/user/NathanielWeiner) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to collect health metrics from WHOOP, Oura, and Withings, normalize them into a daily JSON record, and produce a concise Markdown morning brief. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive biometric and health-provider data. <br>
Mitigation: Install only after reviewing the requested provider access and run it in contexts where that health data is expected to be available. <br>
Risk: The skill stores and refreshes durable OAuth credentials. <br>
Mitigation: Use dedicated 1Password vault items where possible, check permissions on ~/.openclaw/secrets/health_tokens.json, and revoke provider tokens when the skill is no longer used. <br>
Risk: Broad secrets files can expose unrelated credentials to automated sessions. <br>
Mitigation: Avoid sourcing broad secrets files in automated agent sessions; provide only the provider credentials required for the health brief. <br>


## Reference(s): <br>
- [OpenClaw Health page](https://clawhub.ai/NathanielWeiner/openclaw-health) <br>
- [1Password conventions](docs/1PASSWORD_CONVENTIONS.md) <br>
- [Morning brief format](docs/MORNING_BRIEF.md) <br>
- [Oura connector notes](docs/OURA.md) <br>
- [WHOOP connector notes](docs/WHOOP.md) <br>
- [Withings connector notes](docs/WITHINGS.md) <br>
- [OpenClaw cron documentation](https://docs.openclaw.ai/automation/cron) <br>
- [WHOOP developer portal](https://developer.whoop.com) <br>
- [Oura API documentation](https://cloud.ouraring.com/v2/docs) <br>
- [Withings developer portal](https://developer.withings.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a normalized daily health JSON file and a concise Markdown brief when run with configured provider credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
