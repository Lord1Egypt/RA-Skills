## Description:

Universal HiDPI mouse click handling for Linux desktop automation. Auto-detects scale factor or allows calibration for any screen resolution/DPI. Converts Claude display coordinates to xdotool screen coordinates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeyuyuyu](https://clawhub.ai/user/zeyuyuyu)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill to translate displayed screenshot coordinates into Linux/X11 mouse actions on standard and HiDPI desktops. It supports calibrated clicking, movement, dragging, and scale-factor checks when automating desktop workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mouse automation can move or click in sensitive desktop contexts.

Mitigation: Use only in desktop sessions where agent mouse control is acceptable, and avoid sensitive prompts, financial screens, and account-management workflows.

Risk: Unsafe coordinate input handling could misdirect clicks or enable command execution in some uses.

Mitigation: Pass only plain numeric coordinates and harden scripts with strict coordinate validation before relying on them in untrusted-content environments.

Risk: Shared temporary cache files can create risk in multi-user environments.

Mitigation: Use private per-user cache and temporary paths before deployment on shared systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zeyuyuyu/skills/hidpi-mouse)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Linux/X11 desktop automation commands and optional per-user scale calibration.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
