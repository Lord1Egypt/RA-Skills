## Description:

图片尺寸调整和压缩工具技能，用于按指定像素宽高、比例或最大尺寸限制调整图片大小，并支持智能压缩到指定文件大小。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to resize, crop, convert, and compress image files for thumbnails, social media assets, web delivery, and file-size limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: npm install fetches the sharp dependency without a lockfile.

Mitigation: Install in a controlled project or sandbox and review or pin dependencies before using the skill in a production workflow.

Risk: Untrusted images or extreme resize values may create avoidable resource pressure.

Mitigation: Avoid processing untrusted images and apply reasonable input size and dimension limits before running the script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuchubuzai2018/skills/image-resizer)
- [Publisher profile](https://clawhub.ai/user/wuchubuzai2018)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated local image files from the bundled Node.js script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can write resized, cropped, converted, or compressed image files to a requested output path.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
