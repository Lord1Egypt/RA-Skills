## Description: <br>
Track Chinese packages with the Kuaidi100 API, receive push updates, manage tracked packages, and optionally sync delivery reminders to Google Calendar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rou-assistant-bot](https://clawhub.ai/user/rou-assistant-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to subscribe to Kuaidi100 package tracking updates, review locally cached package status, and create optional Google Calendar reminders for same-day deliveries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tracking numbers, carrier data, callback URLs, and package status may be sent to Kuaidi100. <br>
Mitigation: Install only when users are comfortable sharing package tracking data with Kuaidi100, and remove tracked packages when they are no longer needed. <br>
Risk: Optional Google Calendar credentials allow the skill to create or update delivery reminder events. <br>
Mitigation: Configure Google Calendar credentials only when reminder sync is needed and limit calendar access to the intended account or calendar. <br>
Risk: Webhook callbacks rely on a shared token and optional Kuaidi100 signature verification. <br>
Mitigation: Use a strong webhook token, configure a Kuaidi100 salt, and prefer strict signature mode where callback signatures are available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rou-assistant-bot/kuaidi100-tracker) <br>
- [Kuaidi100 API](https://api.kuaidi100.com) <br>
- [Kuaidi100 Subscribe API](https://api.kuaidi100.com/document/subscribeApi) <br>
- [Google Calendar API](https://www.googleapis.com/calendar/v3) <br>
- [Cloudflare Tunnel documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Configuration, API calls] <br>
**Output Format:** [Text responses containing formatted JSON status objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update package tracking state, subscribe to Kuaidi100 callbacks, and create or update Google Calendar delivery reminders when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, openclaw.plugin.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
