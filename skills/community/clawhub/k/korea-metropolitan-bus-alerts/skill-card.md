## Description: <br>
Create and manage scheduled bus arrival alerts using Korea TAGO (국토교통부) OpenAPI and Clawdbot cron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hsooooo](https://clawhub.ai/user/Hsooooo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and Clawdbot operators use this skill to register weekday, weekend, or daily bus-arrival alerts for Korean metropolitan routes and receive scheduled DM summaries through their configured Gateway messaging. <br>

### Deployment Geography for Use: <br>
South Korea <br>

## Known Risks and Mitigations: <br>
Risk: The helper can list or remove Clawdbot cron jobs beyond this bus-alert skill. <br>
Mitigation: Review generated cron jobs before adding them and confirm list or remove operations before execution. <br>
Risk: The DM-only delivery promise depends on the chosen delivery target and is not fully enforced by the helper. <br>
Mitigation: Confirm the delivery target is the registering user's DM before scheduling an alert. <br>
Risk: TAGO_SERVICE_KEY is required for API access and could be exposed through local environment files or copied command output. <br>
Mitigation: Use a dedicated TAGO key where possible and keep local env files and cron exports private. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hsooooo/korea-metropolitan-bus-alerts) <br>
- [TAGO API Reference](references/api_reference.md) <br>
- [Cron recipe](references/cron_recipe.md) <br>
- [TAGO bus stop information API](https://www.data.go.kr/data/15098534/openapi.do) <br>
- [TAGO bus arrival information API](https://www.data.go.kr/data/15098530/openapi.do) <br>
- [BusSttnInfoInqireService endpoint](https://apis.data.go.kr/1613000/BusSttnInfoInqireService) <br>
- [ArvlInfoInqireService endpoint](https://apis.data.go.kr/1613000/ArvlInfoInqireService) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, JSON cron job payloads, and short bus-arrival text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAGO_SERVICE_KEY and a Clawdbot cron/Gateway environment for scheduled delivery.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
