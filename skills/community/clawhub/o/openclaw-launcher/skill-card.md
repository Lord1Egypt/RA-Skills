## Description: <br>
Creates Windows desktop shortcuts and scripts for one-click OpenClaw Gateway startup on WSL, including service start, local port proxy setup, keep-alive handling, and browser launch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinl1993](https://clawhub.ai/user/kevinl1993) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create or repair a Windows launcher for OpenClaw Gateway running in WSL. It is also used to troubleshoot gateway disconnects, gateway stopping behavior, missing shortcut icons, and batch or PowerShell script errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The launcher reads a local OpenClaw token and places it in a local browser URL. <br>
Mitigation: Review the generated PowerShell script before running it, avoid sharing logs or browser URLs containing the token, and keep generated scripts in a user-private directory. <br>
Risk: The launcher uses hidden scripts and a long-running WSL keep-alive process. <br>
Mitigation: Confirm the generated .ps1 and .bat files match the intended behavior, and stop the WSL sleep process or remove the scripts when the launcher is no longer needed. <br>
Risk: The portproxy setup may require administrator approval and changes local networking behavior. <br>
Mitigation: Approve any administrator prompt deliberately, verify the portproxy targets localhost as intended, and inspect current rules with netsh when troubleshooting or removing the launcher. <br>


## Reference(s): <br>
- [ClawHub OpenClaw Launcher Release Page](https://clawhub.ai/kevinl1993/openclaw-launcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with PowerShell, batch, Bash, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-customized launcher scripts and troubleshooting guidance; generated scripts may read a local OpenClaw token, start hidden Windows processes, and request an administrator portproxy change.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
