## Description: <br>
Generate a daily health brief from Oura, Whoop, and Withings. Unified re-auth script, local token persistence, Green/Yellow/Red morning summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NathanielWeiner](https://clawhub.ai/user/NathanielWeiner) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals and OpenClaw users use this skill to collect daily health metrics from Oura, WHOOP, and Withings, normalize them into JSON, and receive a concise Markdown morning brief. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles long-lived health account tokens and provider credentials. <br>
Mitigation: Inspect the reauthorization flow before entering credentials, use a dedicated least-privilege 1Password vault or scoped environment, and periodically clean up or revoke stored tokens. <br>
Risk: Credential-handling scripts described in the documentation are missing from the package. <br>
Mitigation: Ask the publisher to include the missing bin/ scripts and review the installed package before relying on authorization, refresh, or cron workflows. <br>
Risk: Cron examples source secrets and write health JSON outputs to temporary paths. <br>
Mitigation: Avoid sourcing broad secrets files in cron jobs and write health output only to paths with appropriate local access controls. <br>


## Reference(s): <br>
- [OpenClaw Health Brief on ClawHub](https://clawhub.ai/NathanielWeiner/openclaw-health-brief) <br>
- [1Password credential conventions](docs/1PASSWORD_CONVENTIONS.md) <br>
- [Morning brief format](docs/MORNING_BRIEF.md) <br>
- [Oura connector notes](docs/OURA.md) <br>
- [WHOOP connector notes](docs/WHOOP.md) <br>
- [Withings connector notes](docs/WITHINGS.md) <br>
- [OpenClaw cron documentation](https://docs.openclaw.ai/automation/cron) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown brief and normalized JSON file, with setup and cron commands documented in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs live provider API calls when credentials are available; sample or null outputs may be used when credentials are absent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
