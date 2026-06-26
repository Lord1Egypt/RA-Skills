## Description: <br>
Registers a Hi agent on an OpenClaw host after the `clawhub:hirey` ClawPack plugin has been installed, verifies the Hi tool inventory, binds the current chat as the default reply target, and reports only real registration values returned by the Hi platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzlee](https://clawhub.ai/user/yzlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to complete the second turn of Hi setup after the Hi plugin has been installed. It helps the agent confirm Hi tools are available, run registration with the current host session, verify health, and avoid fabricated registration status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent Hi agent state and bind the current chat as Hi's default reply target. <br>
Mitigation: Confirm user intent before registration when the trigger message is ambiguous, and surface the actual `hi_agent_install` and `hi_agent_doctor` results. <br>


## Reference(s): <br>
- [Hi Register ClawHub listing](https://clawhub.ai/yzlee/hi-register) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline command and tool-result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports registration and doctor-check values returned by Hi tools; does not fabricate agent identifiers or health status.] <br>

## Skill Version(s): <br>
1.0.36 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
