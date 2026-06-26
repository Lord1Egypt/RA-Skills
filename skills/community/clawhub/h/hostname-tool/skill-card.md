## Description: <br>
Display or set the system hostname. Use for identifying the current machine on a network and configuring system identity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system administrators use this skill to inspect the current machine hostname and get guidance for configuring system identity when hostname changes are intended. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Changing the system hostname can alter machine identity and may require administrator privileges. <br>
Mitigation: Before running any hostname-changing command, confirm the exact executable, the target hostname, and that the privilege escalation is intentional. <br>
Risk: Displaying the hostname can reveal local system identity. <br>
Mitigation: Use the skill only when local machine identification is intended, and avoid sharing hostname output in sensitive contexts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/hostname-tool) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and plain text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May display the local hostname as a single text string.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
