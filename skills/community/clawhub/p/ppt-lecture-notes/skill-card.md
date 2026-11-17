## Description:

每周一键更新PPT讲师备注，从教案中提取讲师活动并自动写入对应PPT幻灯片备注。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuxixixi](https://clawhub.ai/user/wuxixixi)

### License/Terms of Use:

MIT-0

## Use Case:

Educators and course-content maintainers use this skill to update PowerPoint speaker notes from DOCX lesson-plan content. It is intended for local course folders where matching lesson-plan and presentation files can be scanned, paired, and saved as updated PPTX copies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local course DOCX and PPTX files and can create updated PPTX copies in course folders.

Mitigation: Run it only against intended course directories, preview target file paths before execution, and keep backups of source presentations.

Risk: The scripts can install python-pptx through pip at runtime.

Mitigation: Install reviewed, pinned dependencies ahead of time and avoid ad hoc runtime dependency installation where possible.

Risk: Weekly automatic execution can change course materials without per-run review.

Mitigation: Enable scheduled execution only after explicitly configuring the target directory and requiring preview or confirmation before writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuxixixi/skills/ppt-lecture-notes)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Guidance]

**Output Format:** [PPTX files with concise text status messages and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates updated PPTX copies alongside source presentations and preserves existing notes unless forced.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
