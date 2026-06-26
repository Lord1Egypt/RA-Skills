## Description: <br>
Control and query HomeKit and Home Assistant smart home devices via the Itsyhome macOS app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickustinov](https://clawhub.ai/user/nickustinov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and smart-home operators use this skill to let an agent inspect device state and control HomeKit or Home Assistant devices through the local Itsyhome macOS app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can issue commands for locks, garage doors, and scenes that may affect physical security. <br>
Mitigation: Require explicit user confirmation before unlocking doors, opening garages, or running security-sensitive scenes. <br>
Risk: Debug, camera, live event, and device-state endpoints may expose sensitive home information. <br>
Mitigation: Use these endpoints only when needed and keep the Itsyhome webhook limited to a trusted local environment. <br>


## Reference(s): <br>
- [Itsyhome](https://itsyhome.app) <br>
- [Itsyhome Webhook API Reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/nickustinov/itsyhome-control) <br>
- [Publisher profile](https://clawhub.ai/user/nickustinov) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Itsyhome webhook or URL-scheme actions and should request explicit confirmation for sensitive smart-home operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
