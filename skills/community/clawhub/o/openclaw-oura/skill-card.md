## Description: <br>
Oura Ring data source for OpenClaw (Tier 1). Use to connect an Oura account using an Oura Personal Access Token, fetch Oura v2 usercollection data (sleep, readiness, activity), normalize it into a stable daily JSON shape for the Wellness hub, and render a short summary message for any chat channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gavinchengcool](https://clawhub.ai/user/gavinchengcool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect an Oura account with a Personal Access Token, fetch daily sleep, readiness, and activity data, normalize it for a Wellness hub, and render a short channel-aware summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Oura Personal Access Token grants access to wellness data if exposed. <br>
Mitigation: Store OURA_ACCESS_TOKEN in a protected environment or secret store and rotate it if exposure is suspected. <br>
Risk: Generated raw and normalized JSON files can contain private health and activity data. <br>
Mitigation: Write outputs only to trusted local paths, restrict sharing, and treat generated files as private health data. <br>


## Reference(s): <br>
- [Oura API quick reference](references/oura_api.md) <br>
- [Output schema](references/output_schema.md) <br>
- [Oura API v2 base](https://api.ouraring.com/v2) <br>
- [Publisher profile](https://clawhub.ai/user/gavinchengcool) <br>
- [ClawHub skill page](https://clawhub.ai/gavinchengcool/openclaw-oura) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON files, Shell commands, Configuration] <br>
**Output Format:** [Markdown or plain text summary plus normalized JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OURA_ACCESS_TOKEN; optional OURA_TZ controls date resolution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
