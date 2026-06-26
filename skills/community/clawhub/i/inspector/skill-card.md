## Description: <br>
OpenClaw inspector for registering tracked sessions, inspecting stuck or inactive sessions, checking the current session UUID, listing status, and preparing platform-specific watcher services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netfeel-star](https://clawhub.ai/user/netfeel-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to register OpenClaw sessions for inactivity or recovery monitoring, inspect session status, and prepare a platform-specific watcher service when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session routing details and inspection logs are stored locally in plaintext under the inspector runtime home. <br>
Mitigation: Treat ~/.openclaw/inspector/registry.json and logs as sensitive, restrict local access, and remove or disable registrations when monitoring is no longer needed. <br>
Risk: Incorrect reply channel, account, target, or session identifier could direct inspection messages to the wrong place or fail to monitor the intended session. <br>
Mitigation: Verify trusted runtime metadata before registration, use an actual OpenClaw session UUID, and avoid guessed or placeholder session identifiers. <br>
Risk: Automated monitoring can continue beyond the operator's intended window if sessions remain enabled. <br>
Mitigation: Install and enable monitoring only when intentionally requested, review registered sessions regularly, and unregister or disable sessions after use. <br>


## Reference(s): <br>
- [Inspector Runtime Design](references/config-fields.md) <br>
- [ClawHub skill page](https://clawhub.ai/netfeel-star/inspector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local runtime registry, configuration, state, log, and service-helper files when install or monitoring commands are explicitly invoked.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
