## Description: <br>
Run Kannaka's memory operations on quantum backends, execute OpenQASM circuits, generate quantum random values, and manage qBraid Lab compute and remote coding agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickflach](https://clawhub.ai/user/nickflach) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantum-computing practitioners use this skill to inspect quantum devices, run simulator or explicitly authorized hardware jobs, perform resonance recall experiments, and manage qBraid Lab compute or remote agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start paid qBraid Lab compute that bills by wall-clock minute. <br>
Mitigation: Confirm each paid compute start, require the documented spend opt-in and credit ceiling, list targets first, and explicitly stop compute after use. <br>
Risk: The skill can configure SSH access, inject API keys, and launch remote coding agents. <br>
Mitigation: Confirm SSH setup, credential injection, and agent launches with the user before execution, and limit credentials to the intended remote instance. <br>
Risk: The skill includes environment deletion and kernel removal operations. <br>
Mitigation: List and confirm the exact environment or kernel target before destructive operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nickflach/skills/kannaka-quantum) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON command outputs and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may interact with qBraid, OpenQuantum, SSH, local environment management, and remote agent sessions.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
