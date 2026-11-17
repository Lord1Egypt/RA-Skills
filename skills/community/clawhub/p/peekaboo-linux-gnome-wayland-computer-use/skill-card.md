## Description:

See and control GNOME Wayland desktops using screenshots, ydotool input, Window Calls geometry, AT-SPI hybrid element coordinates, and optional GNOME Remote Desktop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyzcreig](https://clawhub.ai/user/kyzcreig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to set up and operate a GNOME Wayland desktop control loop for screenshot capture, UI element targeting, input injection, remote SSH operation, and optional human RDP access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables remote screen capture and input control on a GNOME desktop.

Mitigation: Install only on machines and user accounts where this control is explicitly authorized.

Risk: Persistent control components such as ydotoold, GNOME extensions, SSH, RDP, or user lingering may remain active after setup.

Mitigation: Disable lingering, ydotoold, RDP, and the GNOME extensions when automation is no longer needed.

Risk: Remote access and credential setup can expose sensitive access paths if configured broadly or handled carelessly.

Mitigation: Keep SSH and RDP LAN- or VPN-scoped, avoid reusing or printing RDP/Linux passwords, and pin and review GNOME extensions before enabling them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyzcreig/skills/peekaboo-linux-gnome-wayland-computer-use)
- [Enabling agent screenshots and input on Ubuntu GNOME/Wayland](references/peekaboo-and-rdp-setup-ubuntu-gnome-wayland.md)
- [Diagnosing gnome-remote-desktop RDP auth failures](references/rdp-auth-diagnosis-server-side.md)
- [Wayland click-by-element hybrid coordinate technique](references/wayland-atspi-hybrid-som.md)
- [allow-gnome-screenshot GNOME extension](https://github.com/siddhpant/allow-gnome-screenshot)
- [Window Calls GNOME extension](https://github.com/ickyicky/window-calls)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup steps, diagnostic procedures, and local helper commands for GNOME Wayland desktop automation.]

## Skill Version(s):

1.0.2 (source: server release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
