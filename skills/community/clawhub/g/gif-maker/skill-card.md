## Description:

将序列帧图片或精灵表（Sprite Sheet）转换为高质量 GIF 动画。支持自定义 FPS、布局切分及循环播放。

This skill is ready for commercial/non-commercial use.

## Publisher:

[guanyang](https://clawhub.ai/user/guanyang)

### License/Terms of Use:


## Use Case:

Developers, creators, and agent users use this skill to convert image sequences or grid sprite sheets into GIF animations with configurable frame rate, layout splitting, looping, and optional size targeting for sticker workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First use may install Python packages into a local virtual environment, and the Pillow dependency is not pinned.

Mitigation: Review package installation policy for the environment and pin or preinstall dependencies before deployment.

Risk: Compression relies on the external gifsicle tool when max-size targeting is requested.

Mitigation: Install gifsicle only from trusted operating-system package sources and verify availability before relying on compression.

Risk: Image processing can expose the runtime to malformed or untrusted input files.

Mitigation: Run the skill on trusted images or inside a contained workspace.

## Reference(s):


## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and generated GIF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local GIF output files from trusted image inputs; optional compression depends on gifsicle.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
