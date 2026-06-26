## Description: <br>
Official Withings OAuth integration for OpenClaw. Use to connect/authorize a personal Withings account, store+refresh tokens locally, and fetch health measurements (weight, body fat, blood pressure, heart rate) plus sleep summaries where available. Supports today/yesterday by timezone and produces normalized daily JSON for the Wellness hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gavinchengcool](https://clawhub.ai/user/gavinchengcool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to authorize a personal Withings account, fetch daily wellness measurements and sleep summaries, normalize the data for the Wellness hub, and render short channel-aware summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Withings OAuth tokens can grant access to personal wellness data if exposed. <br>
Mitigation: Store the token file in a private directory, avoid sharing it, and revoke or rotate the Withings OAuth grant if exposure is suspected. <br>
Risk: Raw and normalized JSON exports may contain sensitive health measurements. <br>
Mitigation: Keep exports in private paths, avoid retained files in shared temporary locations, and delete outputs that are no longer needed. <br>


## Reference(s): <br>
- [Withings API documentation](https://developer.withings.com/) <br>
- [Withings API quick reference](references/withings_api.md) <br>
- [Wellness hub output schema](references/output_schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/gavinchengcool/openclaw-withings) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Text] <br>
**Output Format:** [Shell commands plus JSON data files and text or Markdown summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [OAuth tokens are stored locally; normalized daily output includes sleep, body, and vitals fields when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
