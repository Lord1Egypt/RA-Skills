## Description: <br>
See and control GNOME Wayland desktops using gnome-screenshot, ydotool, Window Calls, AT-SPI hybrid element coordinates, and optional GNOME Remote Desktop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyzcreig](https://clawhub.ai/user/kyzcreig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent inspect and operate a GNOME Wayland desktop for troubleshooting, automation, and remote support workflows. It covers native on-box operation, SSH-driven remote operation, element-targeted clicking, screenshot capture, and optional RDP setup for human access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables unattended screenshot capture and mouse or keyboard control of a logged-in GNOME desktop. <br>
Mitigation: Install it only on systems where agent desktop visibility and control are intended; prefer a dedicated low-privilege account or isolated host. <br>
Risk: Remote-control setup can expose SSH, RDP, ydotoold, lingering sessions, or desktop capture beyond the intended use case. <br>
Mitigation: Keep SSH and RDP scoped to LAN or VPN access, use window-scoped capture where possible, and disable autologin, ydotoold, lingering, and RDP when not actively needed. <br>
Risk: Desktop screenshots may reveal sensitive applications or data in the active user session. <br>
Mitigation: Avoid sensitive apps in the controlled session and review captured outputs before sharing logs, traces, or generated artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kyzcreig/peekaboo-linux-gnome-wayland-computer-use) <br>
- [Publisher profile](https://clawhub.ai/user/kyzcreig) <br>
- [Peekaboo and RDP setup for Ubuntu GNOME Wayland](references/peekaboo-and-rdp-setup-ubuntu-gnome-wayland.md) <br>
- [RDP authentication diagnosis, server side](references/rdp-auth-diagnosis-server-side.md) <br>
- [Wayland click-by-element hybrid coordinate technique](references/wayland-atspi-hybrid-som.md) <br>
- [allow-gnome-screenshot extension](https://github.com/siddhpant/allow-gnome-screenshot) <br>
- [Window Calls extension](https://github.com/ickyicky/window-calls) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands, helper scripts, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Linux desktop-control setup and diagnostic workflows for GNOME Wayland environments.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
