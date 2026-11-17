## Description:

为 3-7 岁儿童生成 L1-L4 识字、描红、组词、古诗诵读和填空的 A4 可打印练习页，包含答案页与家长指导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyumingben](https://clawhub.ai/user/liyumingben)

### License/Terms of Use:

MIT

## Use Case:

Parents, educators, and learning-support agents use this skill to create printable Chinese literacy worksheets and brief parent guidance for preschool and kindergarten learners ages 3-7.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A child's real name can be written into generated local HTML or JSON metadata when the name option is used.

Mitigation: Avoid using a real child name unless local storage of that information is acceptable; use the blank name field or a placeholder for privacy.

Risk: Generated worksheet and metadata files are written to user-selected output paths.

Mitigation: Review output paths before running commands so files are created in the intended workspace location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liyumingben/skills/kindergarten-chinese-course)
- [SkillHub homepage](https://skillhub.cn/skills/user_89a2cacc/kindergarten-chinese-course)
- [识字与诗歌练习页脚本参数与组卷配方](references/activity-spec.md)
- [幼儿识字与诗歌课程大纲](references/curriculum.md)
- [幼儿识字与诗歌家长话术与反馈模板](references/pedagogy.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated worksheet artifacts are local HTML and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated worksheets may include answer pages, scoring fields, pinyin, and reproducibility metadata when a seed or regen JSON is used.]

## Skill Version(s):

1.0.3 (source: frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
