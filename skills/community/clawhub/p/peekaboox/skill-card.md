## Description: <br>
Control and automate the Linux desktop GUI on X11 by taking screenshots, inspecting windows, clicking UI elements, typing text, sending keyboard shortcuts, scrolling, and managing windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gedigi](https://clawhub.ai/user/gedigi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Peekaboox to automate Linux X11 desktop workflows, GUI testing, remote desktop control, and graphical application interactions through shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad local desktop control, including screenshots, window inspection, keystrokes, mouse clicks, and window actions. <br>
Mitigation: Install only in trusted sessions where agent desktop control is intended, and verify the target window before allowing typing or clicking. <br>
Risk: Screenshots and window metadata may contain sensitive information. <br>
Mitigation: Avoid using the skill with password managers, banking sessions, administrative prompts, private chats, or other sensitive windows. <br>
Risk: The skill is limited to X11 and does not support Wayland desktop automation. <br>
Mitigation: Run it only in an X11 session with DISPLAY configured, or use a virtual X11 display such as Xvfb for headless environments. <br>


## Reference(s): <br>
- [Peekaboox on ClawHub](https://clawhub.ai/gedigi/peekaboox) <br>
- [Publisher profile: gedigi](https://clawhub.ai/user/gedigi) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON command output, and screenshot file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Linux X11, DISPLAY, xdotool, wmctrl, and scrot.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
