## Description: <br>
Remote desktop control and automation for capturing screenshots, controlling mouse and keyboard input, automating UI interactions, and managing local desktop tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to let an agent inspect and operate a local desktop session, including screenshots, mouse and keyboard actions, application control, filesystem actions, and scripted workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over a desktop session, including clicking, typing, opening or closing applications, and capturing screenshots. <br>
Mitigation: Use a disposable VM or low-privilege test account, keep sensitive windows closed, and require human review before automation that types, clicks, opens or closes apps, or captures screenshots. <br>
Risk: Automation scripts and file commands can read from or write to user-selected paths. <br>
Mitigation: Restrict allowed scripts and file paths before execution, and review script contents before running them. <br>
Risk: Remote desktop workflows can expose sensitive sessions if VNC or RDP access is configured insecurely. <br>
Mitigation: Use private networks or SSH/VPN tunnels, avoid weak passwords, and do not expose remote desktop ports on public networks. <br>


## Reference(s): <br>
- [OpenClaw Desktop Control on ClawHub](https://clawhub.ai/michealxie001/oc-desktop-control) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python examples, CLI text output, generated files, and base64 screenshot data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform desktop input, capture screenshots, open or close applications, run automation scripts, and read or write local files when invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact package version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
