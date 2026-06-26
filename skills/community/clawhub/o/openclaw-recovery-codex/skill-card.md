## Description: <br>
OpenClaw Gateway recovery and infrastructure diagnostics for Codex agents when Gateway, messaging channels, scheduled tasks, webhook pipelines, or status checks fail across Windows, macOS, and Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShunsukeHayashi](https://clawhub.ai/user/ShunsukeHayashi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to guide Codex through OpenClaw environment discovery, status checks, diagnosis, and recovery reporting for Gateway, channel, service, webhook, configuration, security, and memory issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configuration-changing repair commands may be presented near read-only diagnostics. <br>
Mitigation: Review the exact command and path, back up the configuration, and require explicit approval before running `openclaw doctor --fix` or the BOM-removal snippet. <br>
Risk: Diagnostic output can expose local paths, ports, and network status. <br>
Mitigation: Avoid sharing full diagnostic output publicly and redact sensitive local details before disclosure. <br>
Risk: Service, process, permission, and package modification commands can interrupt Gateway or agent connectivity. <br>
Mitigation: Keep those commands as ACTION_REQUIRED guidance for a human to run in a normal terminal after review. <br>


## Reference(s): <br>
- [Common OpenClaw Failures & Recovery Patterns](artifact/references/common-failures.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ShunsukeHayashi/openclaw-recovery-codex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and structured recovery findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ends with an OpenClaw Recovery Report and uses ACTION_REQUIRED for commands the human should run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
