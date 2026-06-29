## Description: <br>
Kannaka gives agents HRM wave-interference memory, NATS swarm coordination, consciousness metrics, statusline controls, an autonomous coding loop, and optional qBraid quantum tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickflach](https://clawhub.ai/user/nickflach) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Kannaka to add persistent memory recall, swarm sensemaking, status visibility, and optional autonomous coding or quantum-assisted workflows to an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run broad autonomous coding workflows with shell and filesystem access through an external binary. <br>
Mitigation: Use plan mode or scoped working directories when possible, review proposed actions before execution, and avoid yolo mode in sensitive repositories. <br>
Risk: The install path downloads and runs an external kannaka binary. <br>
Mitigation: Confirm the binary source and release verification before installation, and prefer a preapproved KANNAKA_BIN path in managed environments. <br>
Risk: Swarm features can connect to NATS-based peer coordination and exchange sensemaking state. <br>
Mitigation: Join only trusted swarms and disable or avoid swarm commands when project context should remain local. <br>
Risk: qBraid quantum tools can use external services, and hardware QPU choices may spend credits. <br>
Mitigation: Use --no-quantum when quantum tooling is not needed, and keep runs on the free simulator unless hardware use is explicitly approved. <br>


## Reference(s): <br>
- [Kannaka on ClawHub](https://clawhub.ai/nickflach/skills/kannaka) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JSON or NDJSON command output, and configuration updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands shell out to the resolved kannaka binary; status and swarm status provide clean JSON on stdout while boot logs may appear on stderr.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
