## Description: <br>
Manage and run macOS Shortcuts from OpenClaw: list, execute, view details, and sign shortcuts for automation via CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppopen](https://clawhub.ai/user/ppopen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users on macOS use this skill to list, inspect, sign, and run local Shortcuts from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: macOS Shortcuts can execute shell commands, access files, and control other apps with the user's permissions. <br>
Mitigation: Run only trusted shortcuts, inspect unfamiliar shortcuts before execution, and grant Automation, Accessibility, or Full Disk Access only when needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target the user's local macOS Shortcuts library and may require macOS permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
