## Description: <br>
Helps agents onboard OpenClaw configuration clients by collecting requirements, drafting recommended setup options, creating local client records, and preparing quotes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Service providers and OpenClaw implementers use this skill to gather client setup requirements, recommend model and messaging-channel configurations, and prepare client-facing onboarding files and quote drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Client profiles and notes may contain customer data. <br>
Mitigation: Store only necessary details, restrict access to the clients directory, avoid secrets, and delete records when they are no longer needed. <br>
Risk: Generated quotes or contact details may be inappropriate or stale for a specific business. <br>
Mitigation: Review pricing, contact details, and quote drafts before sending them to clients. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/openclaw-client-onboarding) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration content and local file plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce client profile notes, quote drafts, and config.json content under a clients/{customer}/ workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
