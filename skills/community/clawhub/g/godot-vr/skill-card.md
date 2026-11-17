## Description:

Build and headless-verify Godot 4.7 OpenXR/VR apps with room-scale workflow guidance and controller-binding troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueboyzx](https://clawhub.ai/user/blueboyzx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build Godot 4 OpenXR applications, check scenes without a headset, and troubleshoot XR controller tracking and interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project content could be lost when existing files are overwritten.

Mitigation: Review existing files and keep a backup or inspect a diff before applying overwrite steps.

Risk: Changing the machine-wide OpenXR default could affect other XR applications.

Mitigation: Check the current runtime and dependent applications; change the default only when needed and restore it afterward.

Risk: The security review is incomplete because three local references could not be resolved.

Mitigation: Resolve and review the missing reference paths before relying on the affected guidance.

## Reference(s):

- [Godot 4.7 API notes](artifact/references/godot-47-api.md)
- [XR controller troubleshooting](artifact/references/xr-controller-troubleshooting.md)
- [Runtime-swappable graphics styles](artifact/references/style-swap-system.md)

## Skill Output:

**Output Type(s):** [Code, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown with GDScript, Godot project configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a runnable Godot project and verification artifacts such as screenshots.]

## Skill Version(s):

1.0.3 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
