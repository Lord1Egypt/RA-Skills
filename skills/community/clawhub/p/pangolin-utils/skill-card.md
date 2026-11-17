## Description:

Pywayne Visualization Pangolin Utils guides agents in writing Python code with PangolinViewer for real-time 3D visualization of point clouds, trajectories, cameras, planes, chessboards, and images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and robotics or computer vision engineers use this skill to generate code and guidance for visualizing sensor data, SLAM or tracking outputs, robot states, camera calibration scenes, and pose trajectories with pywayne's PangolinViewer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The underlying pywayne/Pangolin dependency may auto-download Pangolin via gettool.

Mitigation: Review and approve dependency download behavior in the target environment before asking an agent to generate or run viewer code.

Risk: Visualization output can be misleading if point, pose, quaternion, or image inputs use unsupported shapes, numeric types, or conventions.

Mitigation: Validate input arrays against the documented float32, SE3, and quaternion format requirements before relying on generated visualization code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyendt/skills/pangolin-utils)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance focuses on pywayne.visualization.pangolin_utils.PangolinViewer usage and expected data formats.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
