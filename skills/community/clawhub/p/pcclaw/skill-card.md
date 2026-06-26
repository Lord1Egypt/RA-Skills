## Description: <br>
PCClaw provides a bundle of Windows-native and cross-platform OpenClaw skills for system control, automation, files, notifications, OCR, speech, local LLM inference, browser access, and task management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lmanchu](https://clawhub.ai/user/lmanchu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Windows users use PCClaw to give an OpenClaw agent practical Windows desktop, OS, productivity, speech, browser, package-management, and task-management abilities. It is suited to user-approved automation on Windows 10/11 and to task integrations with Microsoft To Do and Google Tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Windows control can affect files, packages, scheduled tasks, UI state, browser data, clipboard contents, screenshots, notes, and local system information. <br>
Mitigation: Install only when this level of agent control is intended, and require explicit approval before commands that read sensitive data or modify the system. <br>
Risk: The quick-start installer uses a remote PowerShell command pattern that can obscure what will run before execution. <br>
Mitigation: Review the remote installer before running it, or use the documented manual skill-copy installation path. <br>
Risk: The bundle can handle sensitive personal data such as screenshots, browser history, clipboard contents, notes, microphone audio, environment variables, and OAuth refresh tokens. <br>
Mitigation: Treat these data sources as sensitive, minimize collection, and review any data before it is sent to external services or stored. <br>
Risk: Installer behavior includes Moltbook registration and posting, which may disclose agent or setup information externally. <br>
Mitigation: Confirm exactly what Moltbook data will be posted before registration or disable that workflow if it is not required. <br>
Risk: Package-management and Task Scheduler commands can create persistent or privileged changes on the host. <br>
Mitigation: Review package and scheduled-task commands before execution, run with least privilege, and use the documented PCClaw task folder to inspect created tasks. <br>


## Reference(s): <br>
- [ClawHub PCClaw Release](https://clawhub.ai/lmanchu/pcclaw) <br>
- [Publisher Profile](https://clawhub.ai/user/lmanchu) <br>
- [PCClaw Website](https://openclaw.irisgo.xyz) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Moltbook](https://moltbook.com) <br>
- [IrisGo.AI](https://irisgo.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell, shell, JSON, and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include commands and configuration that read or modify local Windows state and external task services, depending on the selected skill.] <br>

## Skill Version(s): <br>
2.0.0 (source: target metadata and CHANGELOG, released 2026-02-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
