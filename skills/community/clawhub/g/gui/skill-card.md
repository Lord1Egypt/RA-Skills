## Description: <br>
Windows GUI automation toolkit for global hotkeys and window management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyendt](https://clawhub.ai/user/wangyendt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to register Windows global hotkeys, locate and inspect windows, bring windows to the foreground, maximize or close windows, rename windows, and retrieve child-window or geometry information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Window automation can affect the wrong application if a title match is broad or stale. <br>
Mitigation: Confirm the exact target window before automating actions. <br>
Risk: Global hotkey listeners and desktop-control dependencies can continue influencing the desktop after the intended task is complete. <br>
Mitigation: Use a trusted Python environment, avoid administrator privileges unless necessary, and stop the hotkey listener when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyendt/gui) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-only guidance for pywin32, pyuserinput, and pyautogui workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
