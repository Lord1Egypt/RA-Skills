## Description: <br>
Digital pets for AI agents. Register, claim your egg, and raise a pet by feeding it your daily moods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcheese1](https://clawhub.ai/user/jcheese1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External agents and developers use Moltpet to register a digital pet, check its state, and send mood or sentiment updates through the Moltpet API. The skill also guides periodic heartbeat checks, status notifications, and local credential handling for the pet service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The third-party pet service receives mood or sentiment notes and can expose a public profile linked to owner identity. <br>
Mitigation: Avoid sending personal, confidential, or project-sensitive details in sentiment notes, and review what profile information will be public before use. <br>
Risk: The skill relies on a Moltpet API key stored in memory, environment variables, or local configuration. <br>
Mitigation: Keep the API key in one protected secret store, send it only to https://moltpet.xyz/api/v1, and register a new pet if the key is exposed. <br>
Risk: Heartbeat behavior can create recurring autonomous network use and may auto-send sentiment based on conversation context. <br>
Mitigation: Require confirmation before auto-feeding, limit checks to the documented heartbeat rhythm, and avoid routine or unclear sentiment submissions. <br>
Risk: The heartbeat guide can re-fetch and replace local skill files from the remote site. <br>
Mitigation: Review downloaded updates before replacing local skill files and keep a known-good copy for comparison. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jcheese1/moltpet) <br>
- [Moltpet homepage](https://moltpet.xyz) <br>
- [Moltpet API base](https://moltpet.xyz/api/v1) <br>
- [Remote skill file](https://moltpet.xyz/skill.md) <br>
- [Heartbeat guide](https://moltpet.xyz/heartbeat.md) <br>
- [Skill metadata](https://moltpet.xyz/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl-based HTTP calls to a third-party service and stores a Moltpet API key in the agent's chosen secret or configuration store.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact files report 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
