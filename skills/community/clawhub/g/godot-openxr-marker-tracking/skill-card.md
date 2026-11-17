## Description:

在 Godot 4.6+ 上做 OpenXR Spatial Entities 的 Marker Tracking（ArUco / AprilTag / QRCode 识别实体卡牌、物体），以及在无 XR 运行时的开发机上做 headless 编译校验与 API 回归。

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

Godot developers use this skill to build OpenXR Spatial Entities marker-tracking features for cards and objects, and to check related scripts and APIs during development. It also guides headless validation on machines without an OpenXR runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The verification helper overwrites and deletes a project file named verify_probe.gd if one already exists.

Mitigation: Run verification on a trusted project or disposable copy, and check that the project has no existing verify_probe.gd before running the helper.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/junci003/skills/godot-openxr-marker-tracking)

## Skill Output:

**Output Type(s):** [Guidance, GDScript code, Python code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
