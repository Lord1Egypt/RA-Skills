## Description: <br>
Official WHOOP Developer Platform integration for OpenClaw: OAuth connect/authorize, local token storage + refresh, and WHOOP v2 metric fetch (recovery, sleep, strain/cycle, workouts, profile, body measurements). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gavinchengcool](https://clawhub.ai/user/gavinchengcool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect a WHOOP account through the official OAuth flow, fetch recovery, sleep, strain/cycle, workout, profile, and body measurement data, then produce daily or weekly summaries for chat or scheduled delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive health data from WHOOP API responses. <br>
Mitigation: Keep token files and raw JSON exports private, delete raw exports after use, and confirm recipients before enabling cross-channel or scheduled summaries. <br>
Risk: OAuth authorization material may be exposed if redirect URLs or authorization codes are pasted into chat. <br>
Mitigation: Prefer loopback OAuth when available and avoid pasting redirect URLs or authorization codes into chat. <br>
Risk: Overbroad WHOOP scopes can expose more account data than a user needs for a summary. <br>
Mitigation: Request only the minimum WHOOP scopes needed for the intended workflow. <br>
Risk: Timezone defaults can produce a summary for the wrong local day. <br>
Mitigation: Set WHOOP_TZ explicitly and verify the date range before using scheduled summaries. <br>


## Reference(s): <br>
- [WHOOP API quick reference](references/whoop_api.md) <br>
- [Normalized output schema](references/output_schemas.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [WHOOP OpenAPI specification](references/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown summaries, normalized JSON files, and executable shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can render channel-specific message text for generic, Discord, Slack, WhatsApp, or Telegram delivery.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
