## Description: <br>
Official Fitbit OAuth integration for OpenClaw (Tier 1). Use to connect/authorize Fitbit, store+refresh tokens locally, fetch daily activity + sleep summaries, normalize into a stable daily JSON shape for the Wellness hub, and render a short digest for any chat channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gavinchengcool](https://clawhub.ai/user/gavinchengcool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to authorize Fitbit access, fetch daily activity and sleep data, normalize it into a stable Wellness hub JSON shape, and render a short text or Markdown digest for chat channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default Fitbit scopes request broader health and profile access than the daily activity and sleep workflow may need. <br>
Mitigation: Review the Fitbit consent screen and set FITBIT_SCOPES to the minimum permissions needed, likely activity and sleep for this workflow. <br>
Risk: Fitbit tokens and raw health outputs are sensitive if stored in shared or exposed locations. <br>
Mitigation: Use a private FITBIT_TOKEN_PATH, avoid writing raw output to shared locations, and override FITBIT_TZ for the user's actual timezone. <br>


## Reference(s): <br>
- [Fitbit API quick reference](references/fitbit_api.md) <br>
- [Output schema for Wellness hub](references/output_schema.md) <br>
- [ClawHub release page](https://clawhub.ai/gavinchengcool/openclaw-fitbit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown or plain text digest, plus JSON files from fetch and normalization scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Fitbit OAuth client settings and stores refreshed tokens at the configured local token path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
