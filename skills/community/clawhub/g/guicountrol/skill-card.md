## Description: <br>
Control Linux desktop applications through X11/GNOME window management, input simulation, UI hierarchy inspection, and screenshots using xdotool, wmctrl, dogtail, and scrot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dreamtraveler13](https://clawhub.ai/user/dreamtraveler13) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent interact with non-browser Linux GUI applications, including focusing windows, clicking, typing, pressing keys, inspecting accessible UI trees, and capturing screenshots for visual tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Desktop automation can click, type, or press keys in the wrong window. <br>
Mitigation: List and confirm windows before acting, activate only the intended target window, and review planned input actions before execution. <br>
Risk: Screenshots and UI inspection can expose passwords, private data, or unrelated sensitive windows. <br>
Mitigation: Close or hide unrelated sensitive windows and avoid visible credentials or private data before taking screenshots or dumping UI trees. <br>
Risk: Restarting applications to enable accessibility can disrupt active sessions. <br>
Mitigation: Use accessibility restart steps only when needed, target the intended application, and confirm before terminating or relaunching an app. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dreamtraveler13/guicountrol) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text, Files] <br>
**Output Format:** [Markdown with inline shell commands and text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create screenshot files and text UI-tree dumps when invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and release changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
