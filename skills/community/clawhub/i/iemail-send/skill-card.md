## Description: <br>
Send transactional email via Iemail OpenAPI. Configure via OpenClaw skill env only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack-atlas](https://clawhub.ai/user/jack-atlas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to let an agent send single transactional emails through DmartechX/Iemail OpenAPI with configured Iemail credentials and sender settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad credential-file access guidance and requires email API credentials. <br>
Mitigation: Prefer injected IEMAIL_ACCESS_KEY, IEMAIL_ACCESS_KEY_SECRET, and IEMAIL_SENDER values, protect API keys, and confirm each recipient and message body before sending. <br>
Risk: The Python script may install packages at runtime. <br>
Mitigation: Review before installing and prefer a version with pinned dependencies instead of runtime pip installation. <br>
Risk: Email content may include sensitive or regulated information. <br>
Mitigation: Avoid sending sensitive or regulated content unless the provider and workflow are approved for that data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jack-atlas/iemail-send) <br>
- [DmartechX/Iemail Application](https://app.dmartech.cn/) <br>
- [Iemail API Endpoint](https://iemail-api.dmartech.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the IEMAIL_ACCESS_KEY, IEMAIL_ACCESS_KEY_SECRET, and IEMAIL_SENDER environment variables.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
