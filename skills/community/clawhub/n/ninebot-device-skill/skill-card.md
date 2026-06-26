## Description: <br>
ninebot-device-skill helps agents query authorized Ninebot electric vehicle status, charging state, battery level, range, remaining charge time, and location using a Ninebot Device Service key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ninebot-app](https://clawhub.ai/user/ninebot-app) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve Ninebot vehicle telemetry for vehicles they own or are authorized to access, including power, charging, battery, mileage, remaining charge time, and location details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ninebot Device Service keys can grant access to vehicle telemetry. <br>
Mitigation: Prefer the NINEBOT_DEVICESERVICE_KEY environment variable, keep any config.json private and out of source control, and rotate the key if it may have been exposed. <br>
Risk: Vehicle location and telemetry can reveal sensitive personal or operational information. <br>
Mitigation: Run location queries only for vehicles the user owns or is authorized to access, and avoid storing or sharing returned telemetry unnecessarily. <br>
Risk: Misconfigured or stale API mappings could send requests to an unintended service endpoint. <br>
Mitigation: Verify configured endpoints and API mappings still point to the intended Ninebot service before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ninebot-app/ninebot-device-skill) <br>
- [Ninebot API assumptions](references/api-spec.md) <br>
- [Ninebot Device Service endpoint](https://cn-cbu-gateway.ninebot.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NINEBOT_DEVICESERVICE_KEY; returned vehicle telemetry and location data should be treated as sensitive.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
