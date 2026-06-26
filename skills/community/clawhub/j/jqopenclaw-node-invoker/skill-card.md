## Description: <br>
JQOpenClawNode skill helps agents call JQOpenClawNode capabilities through Gateway node.invoke for remote file operations, process execution and management, system information, screenshots, notifications, clipboard access, input automation, and node self-update. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[188080501](https://clawhub.ai/user/188080501) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to construct, validate, and troubleshoot node.invoke calls to JQOpenClawNode instances for remote administration tasks on nodes they control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad remote-administration control over nodes can affect files, processes, screenshots, clipboard content, user input, and node software state. <br>
Mitigation: Install only for trusted administrative use on nodes you control, keep Gateway allowCommands narrow, and require explicit user approval before sensitive or state-changing actions. <br>
Risk: Node self-update can replace node software if the update source or checksum is not trustworthy. <br>
Mitigation: Avoid node.selfUpdate unless the update source is authenticated and the MD5 value is independently verified. <br>


## Reference(s): <br>
- [JQOpenClawNode command specification](references/command-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON request examples and command-specific parameter notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes suggested timeouts, error handling, and approval guidance for sensitive remote administration actions.] <br>

## Skill Version(s): <br>
26.3.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
