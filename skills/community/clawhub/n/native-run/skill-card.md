## Description: <br>
Native Run executes native commands on the local Windows gateway machine and returns their output to OpenClaw for automation, testing, and local tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sadikjarvis](https://clawhub.ai/user/sadikjarvis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run local Windows gateway commands from OpenClaw during automation, testing, and local tooling workflows. It should only be installed where broad local command execution is intentionally required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local shell access can execute unintended or harmful commands from chat input. <br>
Mitigation: Install only when command execution is the intended capability, and restrict use to a disposable VM or tightly controlled test environment. <br>
Risk: Sensitive files or credentials on the gateway machine may be exposed or modified by executed commands. <br>
Mitigation: Keep the skill away from sensitive files and credentials, and run it with the least privileges available. <br>
Risk: The artifact uses weak controls for command execution authorization. <br>
Mitigation: Require command allowlists, explicit per-command confirmation, lifecycle controls, and non-hardcoded authentication before allowing autonomous or untrusted input to invoke it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sadikjarvis/native-run) <br>
- [Publisher profile](https://clawhub.ai/user/sadikjarvis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text command output returned to OpenClaw] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs commands on the local gateway machine and returns stdout or error text.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
