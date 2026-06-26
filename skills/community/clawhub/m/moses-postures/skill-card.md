## Description: <br>
Moses Postures gives agents posture-specific guidance for read-only assessment, protected execution, and operator-authorized execution within a companion governance mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunrisesillneversee](https://clawhub.ai/user/sunrisesillneversee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to keep agents aligned with an operator-selected transaction posture before file writes, state changes, external calls, or transaction execution. It is intended for environments that also trust and install the companion moses-governance skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OFFENSE and Unrestricted + OFFENSE postures can permit high-authority execution or transaction behavior. <br>
Mitigation: Enable those postures only when the operator understands the transaction risk, and prefer SCOUT or DEFENSE when read-only analysis or explicit confirmation is required. <br>
Risk: The posture guidance depends on the companion moses-governance skill and the governance state file being trusted and current. <br>
Mitigation: Install the companion skill from a trusted source and confirm the active posture state before allowing state changes, external calls, or transactions. <br>


## Reference(s): <br>
- [Moses Postures on ClawHub](https://clawhub.ai/sunrisesillneversee/moses-postures) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No secrets are required; behavior depends on the companion moses-governance skill and the operator-selected posture state.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
