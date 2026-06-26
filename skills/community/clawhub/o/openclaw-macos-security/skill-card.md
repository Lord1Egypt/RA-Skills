## Description: <br>
macOS security monitoring for OpenClaw <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drg3nz0](https://clawhub.ai/user/drg3nz0) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this OpenClaw skill to check local macOS camera, microphone, firewall, VPN, open-port, and WiFi status through simple agent commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security review says the skill materially overstates its macOS security capabilities while requesting local command-execution permissions. <br>
Mitigation: Review before installing, treat results as narrow local status checks, and do not rely on the skill for app removal, keylogger/rootkit detection, or broad macOS protection unless those features are separately verified. <br>
Risk: The skill requires local command execution, file-read access, and network permissions. <br>
Mitigation: Install only in environments where those permissions are acceptable, and review the listed local commands before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/drg3nz0/openclaw-macos-security) <br>
- [npm package](https://www.npmjs.com/package/openclaw-macos-security) <br>
- [MaclawPro website](https://maclawpro.com) <br>
- [MaclawPro pricing](https://maclawpro.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted status messages from local macOS command checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include status labels, detected app or port counts, remediation guidance, and product upgrade links.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
