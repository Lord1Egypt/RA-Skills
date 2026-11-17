## Description:

压缩 PPTX 演示文稿文件体积，通过压缩内嵌图片和视频、清理冗余数据、优化 ZIP 打包等手段显著减小 .pptx 文件大小。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyifm](https://clawhub.ai/user/liyifm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to reduce PPTX presentation size by recompressing embedded images and optional videos, removing selected metadata, and writing a compressed copy. It is useful when an agent needs to prepare smaller presentation files for sharing or storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lossy image and video compression can reduce presentation quality or change media fidelity.

Mitigation: Keep the original PPTX and review the compressed output before distribution.

Risk: Optional settings can remove document thumbnails or slide comments.

Mitigation: Use conservative compression settings when comments, thumbnails, or review metadata must be preserved.

Risk: Very large or untrusted PPTX archives can create resource-use or archive-processing risk.

Mitigation: Prefer trusted presentations, avoid unexpectedly large inputs, and run compression in a controlled local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liyifm/skills/ppt-compressor)
- [ffmpeg Windows builds](https://www.gyan.dev/ffmpeg/builds/)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and generated PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local compressed .pptx files and console summaries; video compression depends on ffmpeg availability.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact frontmatter metadata lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
