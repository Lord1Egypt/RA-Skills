## Description: <br>
OpenClaw PC Control lets an agent operate a Windows PC through local CLI and HTTP API actions for screenshots, keyboard and mouse control, clipboard access, file operations, process and window management, browser automation, and shell commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukenccode](https://clawhub.ai/user/lukenccode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users who intentionally install a Windows remote-control skill use it to let an agent inspect and operate a desktop through local API or CLI actions. Typical tasks include taking screenshots, sending keyboard and mouse input, reading or writing files, managing processes and windows, automating a browser, and running shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes host-control actions including shell execution, file writes, process termination, clipboard access, screenshots, and browser JavaScript execution. <br>
Mitigation: Install only when this control surface is intended, keep the API local unless network access is required, and review each proposed host action before execution. <br>
Risk: The artifact includes a bundled API key and the security evidence describes weak/default authentication. <br>
Mitigation: Rotate the API key before use and require bearer-token authentication for any non-public endpoint. <br>
Risk: Disabled or relaxed security modes reduce sandboxing for high-impact host operations. <br>
Mitigation: Use strict mode for normal operation and avoid disabled or relaxed mode unless operating in an isolated test environment. <br>


## Reference(s): <br>
- [PC Control API documentation](references/api-doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/lukenccode/openclaw-pc-control) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands, HTTP API examples, and JSON request or response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions and command/API invocations for host-control workflows; API responses use success, data, and error fields.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
