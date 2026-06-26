## Description: <br>
Web Gateway is a lightweight Flask browser chat interface for a configured OpenClaw HTTP endpoint, with multi-user state, persistent local memory, and optional Google Maps route actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeanne0r](https://clawhub.ai/user/jeanne0r) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a local household-style browser chat gateway for OpenClaw. It supports participant-aware chat, local memory/state files, configurable upstream agent settings, and optional route-opening actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The gateway can persist sensitive household, location, profile, and preference details in local memory and state files. <br>
Mitigation: Review and periodically delete memory/state files, and avoid entering sensitive details unless local retention is intended. <br>
Risk: The Flask service exposes state-changing endpoints without built-in authentication when run. <br>
Mitigation: Bind the service to localhost or place it behind authentication before exposing it beyond a trusted machine. <br>
Risk: Optional Google Maps route support can process location-related details. <br>
Mitigation: Use a restricted Google Maps browser key and limit route features to trusted participants. <br>
Risk: Dependencies are specified as lower bounds rather than pinned versions. <br>
Mitigation: Pin and audit dependencies before deployment outside a trusted local environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jeanne0r/openclaw-web-gateway) <br>
- [Publisher profile](https://clawhub.ai/user/jeanne0r) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration] <br>
**Output Format:** [Browser chat UI with JSON API responses for chat, state, and route actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists local state and memory files under the configured memory directory.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
