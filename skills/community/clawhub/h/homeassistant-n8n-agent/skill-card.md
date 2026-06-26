## Description: <br>
Bridge OpenClaw with your n8n instance for Home Assistant automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enchantedmotorcycle](https://clawhub.ai/user/enchantedmotorcycle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to route Home Assistant state, action, historical, and calendar requests from OpenClaw to a local n8n webhook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can pass smart-home action requests to a local n8n workflow through raw curl calls. <br>
Mitigation: Use only with a trusted n8n workflow, restrict allowed devices and actions in n8n, and require explicit confirmation before action requests are executed. <br>
Risk: Home activity, device state, and calendar prompts may be stored in n8n execution logs. <br>
Mitigation: Limit sensitive prompt content, review n8n retention settings, and handle execution logs according to the user's privacy requirements. <br>
Risk: Prompt text embedded into shell commands can be unsafe if JSON is constructed by interpolation. <br>
Mitigation: Construct JSON safely before invoking curl and validate requestType values before sending webhook requests. <br>


## Reference(s): <br>
- [n8n](https://n8n.io/) <br>
- [ClawHub skill page](https://clawhub.ai/enchantedmotorcycle/homeassistant-n8n-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash curl commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and a trusted local n8n workflow listening on localhost.] <br>

## Skill Version(s): <br>
1.0.4 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
