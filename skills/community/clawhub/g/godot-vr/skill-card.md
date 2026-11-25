## Description:

Build & headless-verify Godot 4.7 OpenXR/VR apps — room-scale workflow, Pimax Crystal tested in-visor, controller-binding pitfalls covered.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueboyzx](https://clawhub.ai/user/blueboyzx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building Godot 4.7 VR or OpenXR applications use this skill to scaffold scenes, configure controller bindings, and verify builds and screenshots on Windows. It also helps diagnose Godot 4.7 rendering, physics, and XR API issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Replacing an existing project file could lose its contents if the write fails or is interrupted.

Mitigation: Back up the target to scratch before replacement, and restore it from that backup if the replacement fails or is interrupted.

Risk: Switching the OpenXR runtime changes the machine-wide default runtime on Windows.

Mitigation: Record the current runtime value before switching and restore that value when finished; account for XR_RUNTIME_JSON overrides.

## Reference(s):

- [Godot 4.7 API forms](references/godot-47-api.md)
- [XR controller troubleshooting](references/xr-controller-troubleshooting.md)
- [Runtime-swappable graphics styles](references/style-swap-system.md)
- [GLB triangle scanner](scripts/scan_glb.py)
- [ClawHub skill listing](https://clawhub.ai/blueboyzx/skills/godot-vr)
- [PimaxXR releases (optional third-party runtime)](https://github.com/mbucchia/Pimax-OpenXR/releases)
- [Publisher profile](https://clawhub.ai/user/blueboyzx)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Technical guidance]

**Output Format:** [Markdown guidance with GDScript, project configuration examples, Python utility code, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project files and verification steps tailored to the user's Godot VR task.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter; ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
