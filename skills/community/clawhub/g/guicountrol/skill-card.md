## Description:

Control the Linux desktop GUI using xdotool, wmctrl, and dogtail for non-browser application interaction, mouse and keyboard input simulation, window management, UI hierarchy inspection, and screenshot capture on X11/GNOME.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreamtraveler13](https://clawhub.ai/user/dreamtraveler13)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill to operate Linux desktop applications by focusing windows, sending keyboard and mouse input, inspecting accessible UI trees, and capturing screenshots when text-based inspection is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GUI controls can click, type, focus, move windows, and otherwise act broadly on the live desktop session.

Mitigation: Use only in desktop sessions where broad GUI control is acceptable, verify target windows before acting, and keep important work saved before running automation.

Risk: The screenshot helper can be abused through unsafe filename handling.

Mitigation: Patch or avoid the screenshot helper until it validates filenames and passes an end-of-options marker to scrot.

Risk: Untrusted action arguments could drive unintended desktop input or window changes.

Mitigation: Avoid using untrusted text as action arguments and review commands before execution.

Risk: The accessibility workflow suggests pkill instructions that can terminate running applications.

Mitigation: Save work and confirm the target process before following pkill-based accessibility instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dreamtraveler13/skills/guicountrol)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline bash commands and script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include desktop automation commands that act on the live GUI session.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
