## Description: <br>
Controls Clash for Windows proxy behavior, including starting or stopping proxy routing, checking status, and switching nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IceNoodle](https://clawhub.ai/user/IceNoodle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users running Clash for Windows use this skill to control local proxy routing from an agent conversation, including status checks, enabling or disabling proxy routing, and selecting an automatic proxy node. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change local proxy routing through broad trigger phrases. <br>
Mitigation: Use explicit Clash-specific commands and confirm before enabling, disabling, or switching proxy modes. <br>
Risk: The artifact includes a hardcoded Clash controller secret. <br>
Mitigation: Replace the secret with a private local configuration and avoid exposing the Clash controller on the LAN unless required. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration guidance, API calls] <br>
**Output Format:** [Plain text status and confirmation messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Controls a local Clash REST API on 127.0.0.1 when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
