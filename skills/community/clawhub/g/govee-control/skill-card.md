## Description: <br>
Script-free Govee OpenAPI setup and control guidance for getting a Govee API key, connecting Govee, listing devices, checking state, and sending power, brightness, or color commands with secure key handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cole-Z](https://clawhub.ai/user/Cole-Z) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure secure Govee API access and operate supported Govee devices with manual curl commands. It is intended for listing devices, checking state, and sending one-device-at-a-time control commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Govee API key and can send commands that turn linked devices on or off or change settings. <br>
Mitigation: Install only if comfortable granting that access; keep actions scoped to intended devices and ask before controlling multiple devices or making bulk changes. <br>
Risk: API keys can be exposed if pasted into chat, stored in skill files, or read from unrelated secret locations. <br>
Mitigation: Store GOVEE_API_KEY in a per-user secrets file, load only that variable, and avoid sharing real keys or device identifiers in published artifacts or chat logs. <br>


## Reference(s): <br>
- [Govee Developer Portal](https://developer.govee.com/) <br>
- [Govee OpenAPI Base URL](https://developer-api.govee.com/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/Cole-Z/govee-control) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces manual curl commands and secure local credential-handling guidance; no scripts are generated.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
