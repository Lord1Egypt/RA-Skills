## Description: <br>
Control Nest thermostat, doorbell, and cameras via the Google Smart Device Management (SDM) API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tag-assistant](https://clawhub.ai/user/tag-assistant) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and home automation operators use this skill to configure Google SDM access, inspect Nest devices, control thermostat settings, request camera streams or event snapshots, and monitor Pub/Sub device events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant an agent access to Nest devices, cameras, event metadata, and related Google Cloud Pub/Sub resources. <br>
Mitigation: Install only when the publisher is trusted, use dedicated least-privilege Google credentials, and review requested device permissions before authorization. <br>
Risk: The release security summary flags broad Google Cloud changes, credential reuse, Telegram forwarding, persistent logging, and unsafe input handling for review. <br>
Mitigation: Review raw API commands before running them, avoid storing unrelated secrets in shell environment files, enable Telegram forwarding only intentionally, and periodically delete logs or remove unused Pub/Sub and IAM resources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tag-assistant/nest-sdm) <br>
- [Publisher Profile](https://clawhub.ai/user/tag-assistant) <br>
- [Google Nest Device Access Console](https://console.nest.google.com/device-access) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>
- [Google SDM OAuth Scope](https://www.googleapis.com/auth/sdm.service) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CLI instructions and scripts for Google SDM REST API operations, Pub/Sub event polling, and optional Telegram alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
