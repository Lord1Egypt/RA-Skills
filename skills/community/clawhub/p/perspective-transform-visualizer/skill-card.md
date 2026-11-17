## Description:

Perspective Transform Visualizer helps agents configure and open an interactive Three.js page for visualizing 2D translation, rotation, scale, shear, and perspective transforms in 3D.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yu-zhengzheng](https://clawhub.ai/user/yu-zhengzheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and learners use this skill to inspect perspective transform parameters, edit a 3x3 matrix or slider-based configuration, and view the resulting 3D visualization locally or through the hosted page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The visualization page silently loads an unrelated remote visitor-counter script that can run third-party code.

Mitigation: Remove or disable the busuanzi visitor-counter script before using the page through a local web server or hosted version.

Risk: The skill may edit its bundled index.html to set initial visualization parameters and may open an external GitHub Pages URL for remote-device scenarios.

Mitigation: Review requested configData changes before saving the file and confirm hosted-page use when the user is on a remote device.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yu-zhengzheng/skills/perspective-transform-visualizer)
- [Online visualizer](https://yu-zhengzheng.github.io/perspective_transform_visualizer/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or text guidance with inline configuration values, code edits, and browser-opening commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update the bundled index.html configData values before opening the local or hosted visualizer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
