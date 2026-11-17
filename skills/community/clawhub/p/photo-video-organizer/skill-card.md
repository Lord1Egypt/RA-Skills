## Description:

为多来源大型照片与视频资料库提供地区自适应的拍摄时间与 GPS 修复、去重、归档和导入工作流。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunerdao](https://clawhub.ai/user/sunerdao)

### License/Terms of Use:

MIT

## Use Case:

适用于需要整理多年、多来源照片与视频资料库的个人和团队。使用者可按地区档案恢复拍摄时间与 GPS、核定重复项、整理文件并准备导入手机或云相册。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The organizer may add unapproved move decisions or move files from outside the selected library.

Mitigation: Work on backed-up copies and avoid bulk moves until CSV quoting and library-boundary checks are fixed.

Risk: Cloud uploads preserve photos and their location and time metadata.

Mitigation: Choose the upload destination deliberately.

Risk: An automatic task monitor may act beyond the current job.

Mitigation: Keep any automatic task monitor limited to the current job.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sunerdao/skills/photo-video-organizer)
- [Photo and video organizing guide](references/guide.md)
- [Mainland China region profile](references/region_cn.md)
- [Global region profile](references/region_global.md)
- [ExifTool](https://exiftool.org/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Files, HTML]

**Output Format:** [Markdown instructions, Python scripts, CSV/JSON reports, interactive HTML review pages, and organized photo/video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review candidates before moving; moved files are intended to remain recoverable.]

## Skill Version(s):

2.0.0 (source: CHANGELOG.md, released 2026-10-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
