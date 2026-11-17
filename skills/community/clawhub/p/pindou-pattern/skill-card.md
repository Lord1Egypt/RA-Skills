## Description:

生成拼豆图纸（perler bead pattern），将图片或像素数据量化为真实拼豆色号的 SVG 图纸、HTML 预览、CSV 物料清单和 JSON 网格。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhexin233-ui](https://clawhub.ai/user/zhexin233-ui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert selected images or JSON pixel grids into printable bead-pattern construction files with bead color codes and material counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Large or untrusted image inputs may consume local resources or exercise image parsing edge cases.

Mitigation: Use images or JSON files intentionally selected by the user, avoid huge untrusted PNG files, and keep grid sizes within the documented range.

Risk: The command can write SVG, HTML, CSV, and JSON outputs to paths supplied at runtime.

Mitigation: Choose output paths in a known workspace directory and review generated paths before sharing or opening files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhexin233-ui/skills/pindou-pattern)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files]

**Output Format:** [Markdown guidance with shell commands and generated SVG, HTML, CSV, and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files may include printable SVG diagrams, HTML previews, CSV material lists, and JSON grid data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
